from pathlib import Path
from typing import *

import typer

from ccf_parser import CCF, CCFHeader, Contest

app = typer.Typer(name='contest', help='比赛管理器')


@app.command(name='init', help='创建比赛')
def init_contest_command(
    path: Annotated[Path, typer.Argument(help='比赛文件夹')] = Path('.'),
    autocreate: Annotated[bool, typer.Option(help='自动创建文件夹')] = True
):  # pragma: no cover
    if autocreate:
        path.mkdir(exist_ok=True, parents=True)

    CCF(
        header=CCFHeader(
            name='',
            path=path,
            description='',
            contest_type='OI'
        ),
        contest=Contest(
            problems=[],
            languages=['CPP']
        )
    )

    # TODO: CLI Contest init
