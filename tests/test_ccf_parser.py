import json
import pathlib

import pydantic
import pytest

from ccf_parser import *

data = json.load(pathlib.Path('./tests/environment/ccf.json').open())


def test_ccf():
    ccf = CCF(**data)
    assert ccf.contest.problems[0].judge_config.checkpoints[0].compare(
        '114514') == False
    assert ccf.contest.problems[0].judge_config.checkpoints[0].compare(
        '114514 114514') == True


def test_checkpoint():
    ckpt = CheckPoint(
        input='good',
        answer='good good',
        input_type='STDIN',
        output_type='STDOUT'
    )

    assert ckpt.compare(' good good ') == True
    assert ckpt.compare('good good\n') == True
    assert ckpt.compare('good good') == True
    assert ckpt.compare('good') == False

    ckpt = CheckPoint(
        input='good',
        answer='good good',
        input_type='STDIN',
        output_type='STDOUT',
        input_file=pathlib.Path('hello'),
        output_file=pathlib.Path('hello')
    )

    assert ckpt.input_file is None
    assert ckpt.output_file is None
