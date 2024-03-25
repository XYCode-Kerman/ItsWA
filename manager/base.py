import atexit
import pathlib
import threading

import uvicorn

from utils import manager_logger

from .api import app as api


def _start_server():  # pragma: no cover
    uvicorn.run(api, host="0.0.0.0", port=2568)


def start_server_background():  # pragma: no cover
    server_thread = threading.Thread(
        target=_start_server)
    server_thread.start()
    return server_thread
