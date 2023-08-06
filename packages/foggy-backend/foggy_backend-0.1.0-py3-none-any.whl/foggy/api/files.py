import logging

import falcon
import foggy.filedb

logging.getLogger(__name__).addHandler(logging.NullHandler())


def _lookup_identifier(db, identifier):
    """Raises falcon.HTTPNotFound"""
    try:
        row = db.lookup_identifier(identifier)
    except foggy.filedb.ItemNotFound as exc:
        # TODO: write test that executes these lines
        message = f"{identifier} index not found"
        logging.info(message)
        raise falcon.HTTPNotFound() from exc
    else:
        return row


class File:
    def __init__(self, foggy_root):
        self.foggy_root = foggy_root

    def _get_db(self, device_id):
        return foggy.filedb.FileDB(root=self.foggy_root, device_id=device_id)

    def _lookup_path(self, device_id, identifier):
        db = self._get_db(device_id)
        metadata = _lookup_identifier(db, identifier)
        return db.root_path / metadata["filename"]

    def on_get(self, req, resp, device_id, identifier):
        logging.info(f"sending {device_id}/{identifier}")
        path = self._lookup_path(device_id, identifier)

        if not path.exists():
            message = f"{device_id}/{identifier} not found"
            logging.info(message)
            raise falcon.HTTPNotFound(description=message)

        resp.stream = path.open("rb")

    def on_delete(self, req, resp, device_id, identifier):
        logging.info(f"deleting {device_id}/{identifier}")

        db = self._get_db(device_id)
        db.trash_file(identifier)
        db.mark_as_removed(identifier)

    def on_put(self, req, resp, device_id, identifier):
        logging.info(f"receiving {device_id}/{identifier}")

        db = self._get_db(device_id)
        db.sync_remote_file(identifier, file_like_object=req.bounded_stream)
