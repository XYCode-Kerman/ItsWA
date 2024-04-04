import datetime
import json
import pathlib
import tempfile
import time
import uuid
from pathlib import Path
from typing import *

import pytest
from fastapi.testclient import TestClient

from manager.base import api, start_server_background
from tests.conftest import temp_contest

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


def test_get_contests(api_client):
    contest_path = Path('./config/contests.json').absolute()
    fake_contest = {
        "name": "homo's contest",
        "description": "string",
        "ccf_file": "/tmp/114514"
    }

    data: List[Dict[str, str]] = json.load(contest_path.open())
    data.append(fake_contest)
    json.dump(data, contest_path.open(mode='w'), indent=4, ensure_ascii=False)

    result = api_client.get('/contest/')
    assert fake_contest not in result.json()


def test_delete_empty_contest(api_client, temp_contest):
    result = api_client.delete(f'/contest/?path=/tmp/114514')
    assert result.status_code == 404

    temp_contest.joinpath('ccf.json').unlink()
    result = api_client.delete(f'/contest/?path={temp_contest}')
    assert result.status_code == 404


def test_delete_contest(api_client, temp_contest):
    result = api_client.delete(f'/contest/?path={temp_contest}')
    assert result.status_code == 404


def test_start_judging(api_client, temp_contest):
    result = api_client.post(f'/contest/judge/start?contest_path=/tmp/114514')
    assert result.status_code == 404
    assert result.json()['detail'] == '路径不存在'

    result = api_client.post(f'/contest/judge/start?contest_path=/tmp')
    assert result.status_code == 404
    assert result.json()['detail'] == 'ccf.json 文件不存在'

    result = api_client.post(
        f'/contest/judge/start?contest_path={temp_contest}')
    assert len(result.json()['trackId']) > 0
    assert result.status_code == 200

    # 查询结果
    trackId = result.json()['trackId']

    result = api_client.get(f'/contest/judge/result/error-trackid')
    assert result.status_code == 422

    result = api_client.get(f'/contest/judge/result/{uuid.uuid4()}')
    assert result.status_code == 404

    n = 10

    for i in range(n):  # pragma: no cover
        result = api_client.get(f'/contest/judge/result/{trackId}')
        if result.status_code == 200:
            break
        elif i == n - 1:
            assert result.status_code == 200
        time.sleep(0.5)

    assert result.status_code == 200
