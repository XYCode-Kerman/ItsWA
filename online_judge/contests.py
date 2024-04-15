import json
from pathlib import Path
from typing import *

import fastapi
from fastapi import APIRouter, HTTPException

from .oj_models import OJContest

router = APIRouter(prefix='/contests', tags=['比赛'])


@router.get('/', name='获取注册在 OJ 中的比赛', response_model=List[OJContest])
async def get_contests():
    pass
