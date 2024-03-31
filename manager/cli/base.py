from typing import Optional

import requests
import typer
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from .judge import app as judge_typer

app = typer.Typer()
app.add_typer(judge_typer)


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
