import json
from pathlib import Path
from typing import Annotated, Optional, Union

import typer

from ccf_parser import CCF, JudgingResult
from judge import ReportAnalyze, start_judging
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


@app.command('analyze', help='分析评测报告')
def analyze_command(
    path: Annotated[Path, typer.Argument(help='报告文件')] = Path(
        './judging_results.json'),
    output: Annotated[Path, typer.Argument(
        help='输出报告HTML的地址')] = Path('./report.html'),
):
    if not path.exists():
        raise FileNotFoundError('报告文件不存在')

    if not path.is_file():
        raise IsADirectoryError('报告文件是一个目录')

    manager_logger.info(f'开始分析报告文件 {path}')

    analyze = ReportAnalyze(
        [
            JudgingResult(**x)
            for x in json.loads(path.read_text('utf-8'))
        ]
    )
    report_html = analyze.generate()

    output.write_text(report_html, 'utf-8')

    manager_logger.info('分析完成')
