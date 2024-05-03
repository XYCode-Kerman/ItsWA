import json
import pathlib
import tempfile
import uuid
from pathlib import Path

import pytest

from ccf_parser import CCF, CheckPoint, JudgingResult
from ccf_parser.status import Status
from judge import ReportAnalyze, simple_judging, start_judging
from judge.languages import CPP, Language
from judge.runtime import runtime

# data = json.load(pathlib.Path('./tests/environment/ccf.json').open())
# ccf = CCF(**data)


def test_start_judging(temp_contest: Path):
    ccf = CCF(**json.loads(temp_contest.joinpath('ccf.json').read_text('utf-8')))

    for multi_process_judging in [False, True]:
        results = list(start_judging(ccf, multi_process_judging))

        # 分析
        analyzed = ReportAnalyze(results).generate()


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


def test_simple_judging():
    # AC代码
    ac_code = """
#include <bits/stdc++.h>
using namespace std;

int main()
{
    string s;getline(cin, s);
    cout<<s<<' '<<s;
    return 0;
}
"""

    # 一半WA代码
    half_wa_code = """
#include <bits/stdc++.h>
using namespace std;

int main()
{
    string s;cin>>s;
    cout<<s<<' '<<s;
    return 0;
}
"""

    # 编译失败
    ce_code = """
Big Brother is Watching You!
                —— 1984    George Orwell
"""

    # 运行失败
    re_code = ac_code.replace('return 0', 'return 1')

    language = CPP()
    checkpoints = [
        CheckPoint(
            input='good',
            answer='good good',
            input_type='STDIN',
            output_type='STDOUT'
        ),
        CheckPoint(
            input='bad',
            answer='bad bad',
            input_type='STDIN',
            output_type='STDOUT'
        ),
        CheckPoint(
            input='doubleplus good',
            answer='doubleplus good doubleplus good',
            input_type='STDIN',
            output_type='STDOUT'
        ),
        CheckPoint(
            input='doubleplus ungood',
            answer='doubleplus ungood doubleplus ungood',
            input_type='STDIN',
            output_type='STDOUT'
        )
    ]

    # 测试全AC代码
    all_ac_ckpt_results = list(simple_judging(
        ac_code, language, checkpoints=checkpoints))
    for ckpt_result in all_ac_ckpt_results:
        assert ckpt_result.status == Status.Accepted
        assert ckpt_result.score == ckpt_result.ckpt.ckpt_score

    # 测试一半WA代码
    half_wa_ckpt_results = list(simple_judging(
        half_wa_code, language, checkpoints=checkpoints))
    for ckpt_result in half_wa_ckpt_results[:2]:
        assert ckpt_result.status == Status.Accepted
        assert ckpt_result.score == ckpt_result.ckpt.ckpt_score

    for ckpt_result in half_wa_ckpt_results[2:]:
        assert ckpt_result.status == Status.WrongAnswer
        assert ckpt_result.score == 0

    # 测试CE代码
    ce_ckpt_results = list(simple_judging(
        ce_code, language=language, checkpoints=checkpoints))
    for ckpt_result in ce_ckpt_results:
        assert ckpt_result.status == Status.CompileError
        assert ckpt_result.score == 0

    # 测试RE代码
    re_ckpt_results = list(simple_judging(
        re_code, language=language, checkpoints=checkpoints))
    for ckpt_result in re_ckpt_results:
        assert ckpt_result.status == Status.RuntimeError
        assert ckpt_result.score == 0
