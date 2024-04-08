import zipfile
from pathlib import Path
from typing import Optional

import requests
import typer
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import track
from rich.text import Text

from utils import manager_logger

from ..base import _start_server, start_server_background
from .contest import app as contest_typer
from .judge import app as judge_typer

console = Console()
app = typer.Typer()
app.add_typer(judge_typer)
app.add_typer(contest_typer)


def download_ited():
    ited_zipfile_path = Path('./assets/ited.zip').absolute()
    ited_folder_path = Path('./assets/ited').absolute()

    if not ited_folder_path.exists():
        ited_folder_path.mkdir(parents=True, exist_ok=True)
        ited_zipfile_path.unlink(missing_ok=True)
        ited_zipfile_path.touch()

        res = requests.get(
            'https://mirror.ghproxy.com/https://github.com/XYCode-Kerman/ItsWA-Editor/releases/download/beta-v0.1.1/dist.zip', stream=True)

        fs = ited_zipfile_path.open('wb')
        for data in track(res.iter_content(chunk_size=128), '下载 ItsWA Editor 中', total=round(int(res.headers['Content-Length']) / 128)):
            fs.write(data)
        fs.close()

        with console.status('解压 ItsWA Editor 中'):
            ited_zipfile = zipfile.ZipFile(ited_zipfile_path.__str__(), 'r')
            ited_zipfile.extractall(ited_folder_path.__str__())
            ited_zipfile.close()


@app.command(name='intro', help='查看ItsWA介绍')
def intro():
    md = Markdown(
        """
## 欢迎使用 ItsWA 评测系统
ItsWA是一个基于Python搭建，使用`Lrun`提供安全运行时的Linux下的竞赛代码评测系统。
查看`docs/guide.pdf`获取使用教程
"""
    )

    print(md)


@app.command(name='server')
def start_server_command():  # pragma: no cover
    download_ited()

    manager_logger.info('访问 http://localhost:2568/editor 以访问ItsWA Manager。')
    _start_server()
