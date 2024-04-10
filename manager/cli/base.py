import shutil
import zipfile
from pathlib import Path
from typing import *
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


def _get_ited_artifact() -> Dict[str, Any]:
    artifacts_resp = requests.get(
        'https://api.github.com/repos/XYCode-Kerman/ItsWA-Editor/actions/artifacts')
    artifact = artifacts_resp.json()['artifacts'][0]
    return artifact


def _get_ited_download_url():
    manager_logger.info('获取 ItsWA Editor 下载地址中...')
    artifact = _get_ited_artifact()
    archive_download_url = artifact['archive_download_url']
    manager_logger.info(f'获取到 ItsWA Editor 下载地址: {archive_download_url}')

    archive_resp = requests.get(
        archive_download_url,
        headers={
            # 注意：该 Token 是 XYCode-Kerman 的个人 Token，不要更改！
            'Authorization': 'Bearer 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'
        },
        allow_redirects=False
    )

    if archive_resp.status_code != 302:
        manager_logger.error(
            f'获取 ItsWA Editor 下载地址失败: {archive_resp.status_code}')
    else:
        manager_logger.info(
            f'获取到 ItsWA Editor 下载地址: {archive_resp.headers["Location"]}')
        return archive_resp.headers["Location"]


def download_ited():
    ited_zipfile_path = Path('./assets/ited.zip').absolute()
    ited_folder_path = Path('./assets/ited').absolute()
    ited_artifact_now_id_file = Path('./assets/ited_id.txt')
    ited_artifact_newest_id = _get_ited_artifact()['id']

    if not ited_folder_path.exists() or str(ited_artifact_now_id_file.read_text('utf-8') if ited_artifact_now_id_file.exists() else '') != str(ited_artifact_newest_id):
        manager_logger.info('检测到 ItsWA Editor 需要更新，开始更新...')

        shutil.rmtree(ited_folder_path.__str__(), ignore_errors=True)
        ited_zipfile_path.unlink(missing_ok=True)

        ited_zipfile_path.parent.mkdir(parents=True, exist_ok=True)
        ited_zipfile_path.touch(exist_ok=True)

        res = requests.get(_get_ited_download_url(), stream=True)

        fs = ited_zipfile_path.open('wb')
        for data in track(res.iter_content(chunk_size=128), '下载 ItsWA Editor 中', total=round(int(res.headers['Content-Length']) / 128)):
            fs.write(data)
        fs.close()

        with console.status('解压 ItsWA Editor 中'):
            ited_zipfile = zipfile.ZipFile(ited_zipfile_path.__str__(), 'r')
            ited_zipfile.extractall(ited_folder_path.__str__())
            ited_zipfile.close()

        ited_artifact_now_id_file.write_text(
            str(ited_artifact_newest_id), 'utf-8')


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
