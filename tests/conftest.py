import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator, List

import pytest
from fastapi.testclient import TestClient

from ccf_parser import CCF, ContestIndex
from manager.api import app as api


@pytest.fixture(scope='function')
def temp_contest():
    old_cwd = os.getcwd()

    tmpcon = tempfile.mkdtemp()
    Path(tmpcon).mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        Path('./tests/environment').absolute().__str__(),
        tmpcon,
        dirs_exist_ok=True
    )

    ccf_file = Path(tmpcon).joinpath('ccf.json')
    ccf = CCF(**json.loads(ccf_file.read_text('utf-8')))
    ccf.header.path = tmpcon
    ccf_file.write_text(json.dumps(
        ccf.model_dump(mode='json'), indent=4), 'utf-8')

    contest_indexes_file = Path('./config/contests.json')
    contest_indexes_file.parent.mkdir(parents=True, exist_ok=True)
    if not contest_indexes_file.exists():
        contest_indexes_file.touch()
        contest_indexes_file.write_text('[]', 'utf-8')

    contest_indexes: List[ContestIndex] = [
        ContestIndex.model_validate(x)
        for x in json.loads(contest_indexes_file.read_text('utf-8'))
    ]

    contest_index = ContestIndex(
        name='tmp_contest',
        description='a temp contest',
        ccf_file=ccf_file.parent
    )
    contest_indexes.append(contest_index)

    # 保存
    contest_indexes_file.write_text(json.dumps(
        [x.model_dump(mode='json') for x in contest_indexes], indent=4, ensure_ascii=False
    ))

    os.chdir(tmpcon)
    yield Path(tmpcon).absolute()
    os.chdir(old_cwd)

    shutil.rmtree(tmpcon)
    contest_indexes.remove(contest_index)
    contest_indexes_file.write_text(json.dumps(
        [x.model_dump(mode='json') for x in contest_indexes], indent=4, ensure_ascii=False
    ))


@pytest.fixture(scope='function')
def ccf(temp_contest: Path) -> CCF:
    data = json.loads(temp_contest.joinpath('ccf.json').read_text('utf-8'))
    ccf = CCF(**data)
    return ccf


@pytest.fixture(scope='module')
def api_client():
    yield TestClient(api)
