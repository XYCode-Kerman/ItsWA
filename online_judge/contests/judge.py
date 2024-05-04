from typing import *

import asyncer
from fastapi import APIRouter, Body, Depends

from ccf_parser import CheckPointResult, Problem
from judge import simple_judging
from judge.languages import CPP

from ..utils.dependencies import require_contest_problem

router = APIRouter(prefix='/judge', tags=['评测'])


@router.post('/submit', name='提交题目进行评测', response_model=List[CheckPointResult])
async def submit_problem(code: Annotated[str, Body(title='代码', media_type='text/plain')], problem: Problem = Depends(require_contest_problem)):
    ckpt_results = list(await asyncer.asyncify(simple_judging)(code=code, language=CPP(), checkpoints=problem.judge_config.checkpoints))

    # 抹除测试点数据
    for ckpt_result in ckpt_results:
        ckpt_result.ckpt.input = '测试点输入已经帮你抹掉了捏，快说谢谢 XYCode 🔐'
        ckpt_result.ckpt.answer = '测试点答案已经帮你抹掉了捏，快说谢谢 XYCode 🔐'

    return ckpt_results
