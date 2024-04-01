import json
import pathlib
import tempfile
from pathlib import Path

import pytest

from ccf_parser import CCF, CheckPoint
from ccf_parser.status import Status
from judge import start_judging
from judge.languages import CPP, Language
from judge.runtime import simple_runtime

# data = json.load(pathlib.Path('./tests/environment/ccf.json').open())
# ccf = CCF(**data)


def test_compile(temp_contest: Path):
    _, output_path_a = tempfile.mkstemp()
    _, output_path_b = tempfile.mkstemp()
    _, output_path_c = tempfile.mkstemp()
    _, output_path_d = tempfile.mkstemp()

    with pytest.raises(TypeError):
        Language().compile(pathlib.Path(
            tempfile.mkstemp[1]), pathlib.Path(output_path_a))

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


def test_start_juding(ccf: CCF):
    start_judging(ccf)


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


def test_simple_runtime():
    for input_type in ['STDIN', 'FILE']:
        assert simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/tle'),
            '',
            input_type,
            pathlib.Path('a.in')
        ) == Status.TimeLimitExceeded

        assert simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/re'),
            '',
            input_type,
            pathlib.Path('a.in')
        ) == Status.RuntimeError

        assert type(simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/ac'),
            '',
            input_type,
            pathlib.Path('a.in')
        )) in [Status, str]

    assert simple_runtime(
        pathlib.Path('./tests/environment/executeables_to_test/ac'),
        '',
        input_type,
        pathlib.Path('/tmp/a.in')
    ) == Status.RuntimeError


# def test_safety_runtime_with_lrun():
    # safety_runtime_with_lrun(pathlib.Path('test'), 'test', 'STDIN')


def test_checkpoint_compare():
    ckpt = CheckPoint(
        input='test',
        answer='test test',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare('test test') == True
    assert ckpt.compare(' test test ') == True
    assert ckpt.compare(' test test \n') == True
    assert ckpt.compare(' test test \n\n') == True

    assert ckpt.compare('test2 test') == False
    assert ckpt.compare(' test2 test ') == False
    assert ckpt.compare(' test2 test \n') == False
    assert ckpt.compare(' test2 test \n\n') == False
