import json
import pathlib

from ccf_parser import *

data = json.load(pathlib.Path('./tests/environment/ccf.json').open())


def test_ccf():
    ccf = CCF(**data)
    assert ccf.contest.problems[0].judge_config.checkpoints[0].compare(
        '114514') is False
    assert ccf.contest.problems[0].judge_config.checkpoints[0].compare(
        '114514 114514') is True
