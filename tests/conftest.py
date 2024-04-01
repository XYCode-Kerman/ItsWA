import json
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from ccf_parser import CCF


@pytest.fixture(scope='function')
def temp_contest():
    tmpcon = tempfile.mkdtemp()
    Path(tmpcon).mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        Path('./tests/environment').absolute().__str__(),
        tmpcon,
        dirs_exist_ok=True
    )

    yield Path(tmpcon).absolute()

    # shutil.rmtree(tmpcon)


@pytest.fixture(scope='function')
def ccf(temp_contest: Path) -> CCF:
    data = json.loads(temp_contest.joinpath('ccf.json').read_text('utf-8'))
    ccf = CCF(**data)
    return ccf
