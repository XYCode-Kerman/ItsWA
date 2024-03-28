import datetime
import json
import pathlib
import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient

from manager.base import api, start_server_background

client = TestClient(api)


def test_base():
    assert client.get('/base/ping').status_code == 200
    assert client.get('/base/ping').json()['message'] == 'pong'
    assert abs(datetime.datetime.fromisoformat(client.get(
        '/base/ping').json()['server_time']) - datetime.datetime.now()) < datetime.timedelta(seconds=0.5)


def test_contest():
    tempcon_dirstr = tempfile.mkdtemp()
    tempcon_dir = pathlib.Path(tempcon_dirstr)

    tempcon_ccf = {
        "header": {
            "name": str(uuid.uuid4()),
            "path": str(tempcon_dir.absolute()),
            "description": "string",
            "contest_type": "OI",
            "enable_oj": True
        },
        "contest": {
            "problems": [],
            "languages": [
                "CPP"
            ]
        }
    }

    assert client.get(
        '/contest').json() == json.loads(pathlib.Path('./config/contests.json').read_text(encoding='utf-8'))

    resp = client.post(
        f'/contest?path={tempcon_dir.absolute()}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 200
    assert resp.json()['name'] == tempcon_ccf['header']['name']

    # 目录已存在
    resp = client.post(
        f'/contest?path={tempcon_dir.absolute()}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 400


def test_ccf():
    tempcon_dirstr = tempfile.mkdtemp()
    tempcon_dir = pathlib.Path(tempcon_dirstr)

    # 创建
    tempcon_ccf = {
        "header": {
            "name": str(uuid.uuid4()),
            "path": str(tempcon_dir.absolute()),
            "description": "string",
            "contest_type": "OI",
            "enable_oj": True
        },
        "contest": {
            "problems": [],
            "languages": [
                "CPP"
            ]
        }
    }
    resp = client.post(
        f'/contest?path={tempcon_dir.absolute()}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 200
    assert resp.json()['name'] == tempcon_ccf['header']['name']

    # 测试获取
    # 成功样例
    ccf = tempcon_dir.joinpath('ccf.json').absolute()

    assert tempcon_dir.joinpath('ccf.json').exists() == True
    resp = client.get(f'/contest/ccf?path={ccf.absolute()}')
    assert resp.status_code == 200
    assert resp.json() == json.loads(ccf.read_text(encoding='utf-8'))

    # 失败样例
    assert client.get(
        f'/contest/ccf?path=/tmp/{uuid.uuid4()}').status_code == 404

    ccf2 = ccf.parent.absolute().joinpath("ccf2.json")
    ccf2.touch()
    assert client.get(f'/contest/ccf?path={ccf2}').status_code == 400

    ccf.write_text('114514', encoding='utf-8')
    assert client.get(f'/contest/ccf?path={ccf}').status_code == 400

    ccf.write_text('fdaf456d4f6a54f61d5g4a6poiwpo', encoding='utf-8')
    assert client.get(f'/contest/ccf?path={ccf}').status_code == 400

    # 测试更改
    resp = client.put(
        f'/contest/ccf?path={ccf}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 200

    resp = client.put(
        f'/contest/ccf?path=/tmp/{uuid.uuid4()}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 404

    ccf3 = ccf.parent.joinpath('ccf3.json').absolute()
    ccf3.touch(exist_ok=True)
    resp = client.put(
        f'/contest/ccf?path={ccf3}', content=json.dumps(tempcon_ccf))
    assert resp.status_code == 400
