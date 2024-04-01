import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from ccf_parser import CCF


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

    os.chdir(tmpcon)
    yield Path(tmpcon).absolute()
    os.chdir(old_cwd)

    shutil.rmtree(tmpcon)


@pytest.fixture(scope='function')
def ccf(temp_contest: Path) -> CCF:
    data = json.loads(temp_contest.joinpath('ccf.json').read_text('utf-8'))
    ccf = CCF(**data)
    return ccf
