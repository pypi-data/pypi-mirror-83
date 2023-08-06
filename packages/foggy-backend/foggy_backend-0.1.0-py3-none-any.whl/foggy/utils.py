#!/usr/bin/env python
import logging
import random
import string
import subprocess
from datetime import datetime
from pathlib import Path


from foggy.exception import FoggyException


logging.getLogger(__name__).addHandler(logging.NullHandler())


class SubprocessError(subprocess.SubprocessError, FoggyException):
    pass


def run(args, check=True):
    """Run COMMAND and return lines"""
    logging.debug(f"run:{' '.join(args)}")
    try:
        completed_process = subprocess.run(
            args, universal_newlines=True, capture_output=True
        )
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        logging.debug(f"stdout: {stdout}")
        logging.debug(f"stderr: {stderr}")
        if check:
            completed_process.check_returncode()
    except subprocess.CalledProcessError as error:
        raise SubprocessError(stderr) from error
    return stdout


def path_with_filename_collision_counter(path, counter=1):
    """If path exists a two digit counter is appended to pathname"""
    if not path.exists():
        return path

    name_with_counter = f"{path.stem}_{counter:02}{path.suffix}"
    next_path = path.with_name(name_with_counter)

    if not next_path.exists():
        return next_path

    return path_with_filename_collision_counter(path, counter=counter + 1)


def random_identifier(*, length=30):
    random_string = "".join(random.choice(string.ascii_letters) for i in range(length))
    return random_string


def timestamp_to_filename(timestamp, *, format="%Y%m%d_%H%M%S"):
    dt = datetime.fromtimestamp(timestamp)
    datetime_as_string = dt.strftime(format)
    return Path(f"{dt.year}") / f"{dt.month:02d}" / datetime_as_string
