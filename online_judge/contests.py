import json
from pathlib import Path
from typing import *

import fastapi
from fastapi import APIRouter, HTTPException

import ccf_parser

router = APIRouter(prefix='/contests', tags=['比赛'])


@router.get('/', response_model=List[ccf_parser.CCF])
async def get_contests():
    contest_indexes_path = Path('./config/contests.json')
    contest_indexes = [
        ccf_parser.ContestIndex.model_validate(x)
        for x in json.loads(contest_indexes_path.read_text('utf-8'))
    ]

    ccfs: List[ccf_parser.CCF] = [
        ccf_parser.CCF.model_validate_json(
            x.ccf_file.joinpath('ccf.json').read_text('utf-8'))
        for x in contest_indexes
    ]

    # 抹除题目数据
    for ccf in ccfs:
        ccf.contest.problems = []

    return ccfs
