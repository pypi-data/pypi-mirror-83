#!/usr/bin/env python
# coding: utf-8
"""Package to keep media libraries in sync with a folder structure on disk.

The purpose of this package is to be able to publish photos and videos from
a library of some kind to a folder on a disk. The folder and library can then
be kept in sync and the folder can be shared with e.g. samba.
"""
import hashlib
import io
import logging
import sqlite3
import time
from contextlib import closing, contextmanager
from pathlib import Path
from threading import Lock

from foggy import utils
from foggy.exception import FoggyException

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "CouldNotImportFiles",
    "FileDB",
    "FileDBException",
    "FileIsModifiedBeforeCreated",
    "ItemAlreadyInserted",
    "ItemNotFound",
]
SCHEMA = """
CREATE TABLE IF NOT EXISTS {} (
    identifier          TEXT    NOT NULL UNIQUE,
    filename            TEXT    NOT NULL UNIQUE,
    timestamp           REAL    NOT NULL,
    timestamp_modified  REAL    NOT NULL,
    removed             BOOL,
    nr_of_bytes         INTEGER,
    secure_hash         BLOB
);
"""


class FileDBException(FoggyException):
    pass


class FileIsModifiedBeforeCreated(FileDBException):
    pass


class CouldNotImportFiles(FileDBException):
    pass


class ItemAlreadyInserted(FileDBException):
    pass


class ItemNotFound(KeyError, FileDBException):
    pass


def count_bytes_and_calculate_sha256(path):
    nr_of_bytes = 0
    hasher = hashlib.sha256()
    with path.open(mode="rb") as f:
        bytes_ = f.read(io.DEFAULT_BUFFER_SIZE)
        while bytes_:
            hasher.update(bytes_)
            nr_of_bytes += len(bytes_)
            bytes_ = f.read(io.DEFAULT_BUFFER_SIZE)
    digest = hasher.digest()
    return nr_of_bytes, digest


class FileDB:
    """Database of images and videos on disk."""

    def __init__(self, *, root, device_id):
        self.root_path = Path(root) / device_id
        self.device_id = device_id
        self.db_path = self.root_path / ".foggy" / f"files_{device_id}.db"
        self.remote_db_path = self.root_path / ".foggy" / f"files_{device_id}_remote.db"

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_dir_path.mkdir(exist_ok=True)

        self._connection = sqlite3.connect(
            self.db_path, check_same_thread=False, isolation_level="DEFERRED"
        )
        self._connection.row_factory = sqlite3.Row
        self._lock = Lock()

    def __str__(self):
        return str(self.db_path)

    def __repr__(self):
        # TODO: write test that executes these lines
        return f"{self.__class__.__name__} in {self.__str__()}"

    @property
    def trash_dir_path(self):
        return self.root_path / "trashcan"

    @property
    def cache_dir_path(self):
        return self.root_path / ".cache"

    def _row_to_path(self, row):
        return self.root_path / row["filename"]

    @property
    @contextmanager
    def transaction(self):
        with self._lock:
            try:
                yield
                self._connection.commit()
            except:  # noqa e722
                self._connection.rollback()
                raise

    def create_files_table(self):
        sql_script = SCHEMA.format("local_files")
        with self.transaction:
            self._execute_script(sql_script)

    def _execute_script(self, sql):
        with closing(self._connection.cursor()) as cursor:
            cursor.executescript(sql)

    def _execute(self, sql, parameters=(), fetch_one=False, fetch_all=False):
        with closing(self._connection.cursor()) as cursor:
            cursor.execute(sql, parameters)
            self._connection.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    def get_insertable_path(self, path):
        """If path already exists in the database a two digit counter is appended to
        pathname"""

        path_with_counter = path
        counter = 0

        while self.has_filename(path_with_counter):
            counter += 1
            name_with_counter = f"{path.stem}_{counter:02}{path.suffix}"
            path_with_counter = path.with_name(name_with_counter)

        return path_with_counter

    def convert_to_path_that_can_be_inserted(self, *, timestamp, suffix):
        timestamp_path = utils.timestamp_to_filename(timestamp).with_suffix(suffix)
        return self.get_insertable_path(timestamp_path)

    def insert(
        self,
        *,
        identifier,
        suffix,
        timestamp,
        modified_timestamp=None,
        cached_path=None,
    ):
        """Add file to database

        :identifier:
        :suffix: suffix of file to be added
        :timestamp: time of creation
        :modified_timestamp: time of update
        :cached_path: file to move into target path
        :raises: ItemAlreadyInserted, FileISModifiedBeforeCreated,
                 sqlite3.IntegrityError
        """
        filename = self.convert_to_path_that_can_be_inserted(
            timestamp=timestamp, suffix=suffix
        )
        target_path = self.root_path / filename
        logging.info(f"inserting {identifier} -> ({filename})")

        if modified_timestamp is None:
            modified_timestamp = timestamp

        if cached_path is not None:
            target_path.parent.mkdir(parents=True, exist_ok=True)

            nr_of_bytes, digest = count_bytes_and_calculate_sha256(cached_path)
            cached_path.rename(str(target_path))
        else:
            nr_of_bytes, digest = 0, None

        parameters = (
            identifier,
            str(filename),
            timestamp,
            modified_timestamp,
            False,
            nr_of_bytes,
            digest,
        )
        try:
            with self.transaction:
                self._execute(
                    "INSERT INTO local_files VALUES (?,?,?,?,?,?,?)",
                    parameters=parameters,
                )
        except sqlite3.IntegrityError as error:

            if "UNIQUE constraint failed: local_files.identifier" == error.args[0]:
                raise ItemAlreadyInserted(
                    f"{identifier} is already inserted"
                ) from error

            else:
                # TODO: write test that executes these lines
                raise

    def update(self, *, identifier, cached_path, timestamp):
        """Move CACHED_PATH into target path and update BYTES and HASH in database"""

        row = self.lookup_identifier(identifier)
        target_path = self._row_to_path(row)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        cached_path.rename(str(target_path))
        nr_of_bytes, digest = count_bytes_and_calculate_sha256(target_path)

        parameters = (nr_of_bytes, digest, timestamp, identifier)
        with self.transaction:
            self._execute(
                "UPDATE local_files SET nr_of_bytes=?, secure_hash=?, "
                "timestamp_modified=? WHERE identifier = ?",
                parameters=parameters,
            )

    def mark_as_removed(self, identifier):
        with self.transaction:
            self._execute(
                f"UPDATE local_files SET removed=true WHERE identifier='{identifier}'",
            )

    def lookup(self, field, value, remote=False) -> sqlite3.Row:
        if remote:
            sql = f"SELECT * FROM remote_files WHERE remote_files.{field}=?"
        else:
            sql = f"SELECT * FROM local_files WHERE {field}=?"

        with self.transaction:
            row = self._execute(sql, parameters=(value,), fetch_one=True)
        if row is None:
            raise ItemNotFound(f"found nothing with {sql}={value}")
        else:
            return row

    def update_remote_files_table(self):
        table_name = "remote_files"
        with self.transaction:
            self._execute_script(
                f"DROP TABLE IF EXISTS {table_name}; {SCHEMA.format(table_name)}"
            )
            self._execute(
                "ATTACH DATABASE (?) AS remote", parameters=(str(self.remote_db_path),)
            )
            self._execute("INSERT INTO remote_files SELECT * FROM remote.local_files")
            self._execute("DETACH DATABASE remote")

    def lookup_identifier(self, identifier, remote=False) -> sqlite3.Row:
        return self.lookup("identifier", identifier, remote=remote)

    def lookup_filename(self, filename, remote=False) -> sqlite3.Row:
        return self.lookup("filename", str(filename), remote=remote)

    def has_filename(self, filename) -> bool:
        try:
            self.lookup_filename(filename)
        except ItemNotFound:
            return False
        else:
            return True

    def lookup_all(self) -> list:
        with self.transaction:
            rows = self._execute(
                "SELECT * FROM local_files ",
                fetch_all=True,
            )
            return rows

    def delete(self, identifier):
        with self.transaction:
            self._execute(
                "DELETE FROM local_files WHERE identifier=?", parameters=(identifier,)
            )

    def sync_remote_index(self, file_like_object):
        """Save FILE_LIKE_OBJECT to disc and copy files table to *files_remote* table"""
        self.remote_db_path.write_bytes(file_like_object.read())
        self.update_remote_files_table()

        return self.identifiers_to_be_updated

    @property
    def identifiers_to_be_updated(self):
        with self.transaction:
            remote_modified_rows = self._execute(
                "SELECT remote.identifier, remote.timestamp_modified"
                "   FROM remote_files AS remote"
                "   WHERE remote.removed = false"
                "   EXCEPT"
                "   SELECT local.identifier, local.timestamp_modified"
                "   FROM local_files as local",
                fetch_all=True,
            )
        return {row["identifier"] for row in remote_modified_rows}

    @property
    def identifiers_to_be_removed(self):
        with self.transaction:
            removed_rows = self._execute(
                "SELECT remote.identifier"
                "    FROM remote_files AS remote"
                "    WHERE remote.removed = true"
                "    INTERSECT"
                "    SELECT local.identifier"
                "    FROM local_files as local"
                "    WHERE local.removed = false",
                fetch_all=True,
            )
        return {row["identifier"] for row in removed_rows}

    def sync_remote_file(self, identifier, file_like_object):
        """Insert or update IDENTIFIER with VERSION from remote_files

        :param identifier:
        :param file_like_object:
        """
        remote_row = self.lookup_identifier(identifier, remote=True)

        remote_filename_ = remote_row["filename"]
        suffix_ = Path(remote_filename_).suffix
        timestamp_ = remote_row["timestamp"]
        timestamp_modified_ = remote_row["timestamp_modified"]

        cache_path = self.write_intermediate_file(identifier, file_like_object)

        try:
            self.update(
                identifier=identifier,
                cached_path=cache_path,
                timestamp=timestamp_modified_,
            )
        except ItemNotFound:
            self.insert(
                identifier=identifier,
                suffix=suffix_,
                timestamp=timestamp_,
                modified_timestamp=timestamp_modified_,
                cached_path=cache_path,
            )

    def write_intermediate_file(self, identifier, file_like_object) -> Path:
        """Write FILE_LIKE_OBJECT to disc

        :param identifier:
        :param file_like_object: to call .read() on
        :raises: ItemNotFound
        """
        cache_path = self.cache_dir_path / identifier
        logging.info(f"Writing {identifier}-->{cache_path}")
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(file_like_object.read())
        return cache_path

    def trash_file(self, identifier):
        """Move IDENTIFIER file to trash"""
        try:
            row = self.lookup_identifier(identifier=identifier)
            path = self._row_to_path(row)
            filename = row["filename"]
            trash_path = self.trash_dir_path / filename

            trash_path.parent.mkdir(parents=True, exist_ok=True)
            path.rename(trash_path)
        except ItemNotFound:
            logging.debug(f"{identifier} has not been written to disc yet")
        except FileNotFoundError:
            logging.warning(f"{path} has already been removed")
        else:
            logging.info(f"removed {path}")
