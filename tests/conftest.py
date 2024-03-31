import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


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
