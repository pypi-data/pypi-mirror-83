import json
import logging

import foggy.filedb

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Index:
    def __init__(self, foggy_root):
        self.foggy_root = foggy_root

    def on_put(self, request, response, device_id):
        logging.info(f"Receiving new index from {device_id}")

        db = foggy.filedb.FileDB(root=self.foggy_root, device_id=device_id)

        db.sync_remote_index(file_like_object=request.bounded_stream)

        response_dict = {
            "missing": sorted(db.identifiers_to_be_updated),
            "remove": sorted(db.identifiers_to_be_removed),
        }
        logging.info(f"Missing: {', '.join(response_dict['missing'])}")
        logging.info(f"To be removed: {', '.join(response_dict['remove'])}")
        response.body = json.dumps(response_dict)
