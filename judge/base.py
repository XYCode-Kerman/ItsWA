import datetime
import json
from pathlib import Path
from typing import List

from ccf_parser import CCF
from ccf_parser.results import JudgingResult
from utils import judge_logger

from .player import Player


def start_judging(ccf: CCF):
    start = datetime.datetime.now()
    judging_results: List[JudgingResult] = []
    judge_logger.info(f'开始评测比赛 {ccf.header.name}，当前时间：{start}')

    # 匹配选手列表
    players: List[Player] = []
    for player_dir in ccf.header.path.joinpath('players').iterdir():
        player = Player(
            name=f'选手 {player_dir.name}',
            order=player_dir.name,
            path=player_dir
        )

        judge_logger.info(f'匹配到选手 {player.order} 在目录 {player_dir} 下。')
        players.append(player)

    # 评测
    for player in players:
        result = player.judging(ccf)
        judging_results.append(result)

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
    return judging_results
