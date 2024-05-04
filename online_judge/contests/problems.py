from typing import *

from fastapi import APIRouter, Depends

from ..oj_models import OJContest, OJProblem
from ..utils.dependencies import require_contest_started

router = APIRouter(prefix='/detail', tags=['题目信息'])


@router.get('/{contest_id}/problems', name='获取比赛题目', summary='> 注意：仅当比赛开始后可以调用', response_model=List[OJProblem])
async def get_contest_problems(contest: OJContest = Depends(require_contest_started)):
    return [
        OJProblem.load_from_ccf_problem(x)
        for x in contest.read_ccf.contest.problems
    ]
