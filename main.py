import atexit
import threading

import dotenv
import requests

from ccf_parser import CCF
from configs import TELEMETERING
from manager import cli_app, start_server_background
from telemetering import get_client_id

dotenv.load_dotenv()


def telemetering():
    if TELEMETERING:
        resp = requests.post('http://itte.api.xycode.club/', json={
            'client_id': get_client_id(),
            'event': 'start'
        })


@atexit.register
def _exit():
    if TELEMETERING:
        resp = requests.post('http://itte.api.xycode.club/', json={
            'client_id': get_client_id(),
            'event': 'stop'
        })


if '__main__' == __name__:
    threading.Thread(target=telemetering).start()
    cli_app()
