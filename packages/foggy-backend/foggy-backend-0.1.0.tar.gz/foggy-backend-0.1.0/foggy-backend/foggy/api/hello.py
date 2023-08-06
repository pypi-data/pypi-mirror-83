import json
import logging

import falcon

from foggy.filedb import FileDB

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Hello:
    def __init__(self, foggy_root):
        self.foggy_root = foggy_root

    def on_get(self, req, resp, device_id):
        logging.info(
            f"received Hello from {device_id}, initiating FileDB in {self.foggy_root}"
        )
        try:
            db = FileDB(root=self.foggy_root, device_id=device_id)
            db.create_files_table()
            resp.body = json.dumps({"device_id": db.device_id})

        except Exception as exc:
            logging.error(exc)
            raise falcon.HTTPInternalServerError(description=str(exc))
