import os
from pathlib import Path

import falcon
from foggy.api import files, hello, index

FOGGY_ROOT = os.environ.get("FOGGY_ROOT", default=Path.home() / "pictures")


def create_app():
    api = falcon.API()
    base_url = "/foggy/api/v0.1"

    url_to_handler = {
        "/hello/{device_id}": hello.Hello(FOGGY_ROOT),
        "/index/{device_id}": index.Index(FOGGY_ROOT),
        "/files/{device_id}/{identifier}": files.File(FOGGY_ROOT),
    }
    for url, handler in url_to_handler.items():
        api.add_route(base_url + url, handler)

    return api


def get_app():
    return create_app()
