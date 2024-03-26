import atexit
import pathlib
import threading

import uvicorn

from utils import manager_logger

from .api import app as api


def init_config():  # pragma: no cover
    configdir = pathlib.Path('./config')

    configdir.mkdir(exist_ok=True, parents=True)
    if not configdir.joinpath('contests.json').exists():
        configdir.joinpath('contests.json').touch(exist_ok=True)
        configdir.joinpath('contests.json').write_text('[]', encoding='utf-8')


def _start_server():  # pragma: no cover
    uvicorn.run(api, host="0.0.0.0", port=2568)


def start_server_background():  # pragma: no cover
    server_thread = threading.Thread(
        target=_start_server)
    server_thread.start()
    return server_thread


init_config()
