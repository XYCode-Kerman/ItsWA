import asyncio
import datetime
import json
import threading
from multiprocessing import cpu_count
from pathlib import Path
from typing import *
from typing import List

import anyio
from anyio import to_process
from rich.progress import Progress, track

from ccf_parser import CCF
from ccf_parser.results import JudgingResult
from utils import judge_logger

from .player import Player


def start_judging(ccf: CCF, multi_process_judging: bool = True, judging_process: int = cpu_count() * 2) -> Generator[List[JudgingResult], Any, Any]:
    start = datetime.datetime.now()
    judging_results: List[JudgingResult] = []
    judge_logger.info(f'开始评测比赛 {ccf.header.name}，当前时间：{start}')

    # 匹配选手列表
    players: List[Player] = []
    for player_dir in track(ccf.header.path.joinpath('players').iterdir(), description='匹配选手中...', total=len(list(ccf.header.path.joinpath('players').iterdir()))):
        player = Player(
            name=f'选手 {player_dir.name}',
            order=player_dir.name,
            path=player_dir
        )

        players.append(player)

    # 评测
    if not multi_process_judging:
        for player in players:
            result = player.judging(ccf)
            judging_results.append(result)
            yield result
            judge_logger.info(f'选手 {player.order} 评测完成。')
    else:
        # 多进程并行
        tasks: List[asyncio.Task] = []
        task2player: Dict[asyncio.Task, Player] = {}
        loop = asyncio.new_event_loop()
        limiter = anyio.CapacityLimiter(judging_process)
        for player in players:
            task = loop.create_task(
                to_process.run_sync(player.judging, ccf, limiter=limiter),
            )

            tasks.append(task)
            task2player[task] = player

        threading.Thread(target=loop.run_until_complete,
                         args=(asyncio.wait(tasks),)).start()

        # 未完成就一直检测
        with Progress() as progress:
            judging_progress_task = progress.add_task(
                description=f'评测中...', total=len(tasks))

            while tasks.__len__() > 0:
                for task in tasks:
                    if task.done():
                        result: JudgingResult = task.result()

                        judge_logger.info(
                            f'选手 {task2player[task].order} 评测完成。')
                        yield result

                        progress.advance(judging_progress_task)
                        judging_results.append(result)
                        tasks.remove(task)

    # 保存评测数据
    Path(ccf.header.path).joinpath('./judging_results.json').write_text(
        json.dumps(
            [x.model_dump(mode='json') for x in judging_results],
            indent=4,
            ensure_ascii=False
        ),
        encoding='utf-8'
    )

    end = datetime.datetime.now()
    judge_logger.info(
        f'评测比赛 {ccf.header.name} 完成，当前时间：{end}，总用时：{end - start}')
