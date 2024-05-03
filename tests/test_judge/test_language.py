import pathlib
import tempfile
from pathlib import Path

import pytest

from ccf_parser import CCF
from ccf_parser.status import Status
from judge import start_judging
from judge.languages import CPP, Language


def test_compile(temp_contest: Path):
    _, output_path_a = tempfile.mkstemp()
    _, output_path_b = tempfile.mkstemp()
    _, output_path_c = tempfile.mkstemp()
    _, output_path_d = tempfile.mkstemp()

    # 必定成功
    assert CPP().compile(
        # pathlib.Path('./tests/environment/players/xycode/a/a.cpp').absolute(),
        temp_contest.joinpath('players/xycode/a/a.cpp').absolute(),
        pathlib.Path(output_path_a).absolute()
    ) == True

    # 必定失败，语法错误
    assert CPP().compile(
        # pathlib.Path('./tests/environment/players/xycode/b/b.cpp').absolute(),
        temp_contest.joinpath('players/xycode/b/b.cpp').absolute(),
        pathlib.Path(output_path_b).absolute()
    ) == False

    # 必定失败，源文件不存在
    assert CPP().compile(
        # pathlib.Path('./tests/environment/players/xycode/c/c.cpp').absolute(),
        temp_contest.joinpath('players/xycode/c/c.cpp').absolute(),
        pathlib.Path(output_path_c).absolute()
    ) == False

    # 必定失败，非法代码
    assert CPP().compile(
        # pathlib.Path('./tests/environment/players/xycode/d/d.cpp').absolute(),
        temp_contest.joinpath('players/xycode/d/d.cpp').absolute(),
        pathlib.Path(output_path_d).absolute()
    ) == False


def test_illegal_language(ccf: CCF):
    ccf2 = ccf
    for idx in range(len(ccf2.contest.problems)):
        ccf2.contest.problems[idx].judge_config.languages = ['C']

    # 均为CE
    result = start_judging(ccf2)

    for player in result:
        for problem in player.problems_result.values():
            for ckpt_result in problem:
                assert ckpt_result.status == Status.CompileError
                assert ckpt_result.score == 0
