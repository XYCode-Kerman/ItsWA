import datetime

import pytest
from fastapi.testclient import TestClient

from manager.base import api, start_server_background

client = TestClient(api)


def test_base():
    assert client.get('/base/ping').status_code == 200
    assert client.get('/base/ping').json()['message'] == 'pong'
    assert abs(datetime.datetime.fromisoformat(client.get(
        '/base/ping').json()['server_time']) - datetime.datetime.now()) < datetime.timedelta(seconds=0.5)
