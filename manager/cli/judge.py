import json
from pathlib import Path
from typing import Annotated, Optional, Union

import typer

from ccf_parser import CCF
from judge import start_judging
from utils import manager_logger

app = typer.Typer(name='judge', help='评测相关')


@app.command('start', help='开始评测')
def start_judging_command(path: Annotated[Path, typer.Argument(help='比赛目录或CCF文件')] = Path('.')):
    ccf: Optional[CCF] = None

    if path.name == 'ccf.json':
        ccf = CCF(**json.loads(path.read_text('utf-8')))
    elif path.is_dir() and path.joinpath('ccf.json').exists():
        ccf = CCF(**json.loads(path.joinpath('ccf.json').read_text('utf-8')))
    else:
        raise FileNotFoundError('评测目录不正确，可能是不存在CCF文件')

    start_judging(ccf)
    return 0
