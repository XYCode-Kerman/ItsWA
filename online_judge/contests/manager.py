import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import *

import fastapi
from fastapi import APIRouter, Body, Depends, HTTPException
from tinydb import Query

import ccf_parser

from ..auth import require_role
from ..oj_models import OJContest
from ..utils import contestscol
from ..utils.dependencies import require_ccf_file

router = APIRouter(prefix='/manage')


@router.get('/', name='获取注册在 OJ 中的比赛', response_model=List[OJContest])
async def get_contests():
    return contestscol.all()


@router.post('/', name='在 OJ 中注册一个已存在的比赛', response_model=OJContest, dependencies=[Depends(require_role('admin'))])
async def register_contest_to_oj(
        start_time: Annotated[datetime, Body()],
    end_time: Annotated[datetime, Body()],
    ccf_file: Path = Depends(require_ccf_file)
):
    oj_contest = OJContest(
        contest_id=uuid.uuid4(),
        ccf_file=ccf_file,
        start_time=start_time,
        end_time=end_time
    )

    doc_id = contestscol.insert(oj_contest.model_dump(mode='json'))

    query = Query()
    return contestscol.get(doc_id=doc_id)


@router.put('/{contest_id}', name='更新 OJ 中已注册的比赛', response_model=OJContest, dependencies=[Depends(require_role('admin'))])
async def update_contest_in_oj(contest_id: str, contest: OJContest):
    query = Query()

    doc_id = contestscol.upsert(
        contest.model_dump(mode='json'),
        query.contest_id == contest_id
    )[0]

    return contestscol.get(doc_id=doc_id)


@router.delete('/{contest_id}', name='删除 OJ 中已注册的比赛', dependencies=[Depends(require_role('admin'))], responses={
    200: {
        'description': '成功删除',
        'content': {'application/json': {'example': {'status': True}}}
    }
})
async def delete_contest_in_oj(contest_id: str):
    query = Query()

    contestscol.remove(query.contest_id == contest_id)

    return {
        'status': True
    }
