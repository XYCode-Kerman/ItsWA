import datetime
import uuid
from pathlib import Path

import pydantic
from fastapi import Depends, HTTPException
from tinydb import Query

from ccf_parser import CCF

from ...oj_models import OJContest
from ..database import contestscol


def require_ccf_file(ccf_file: Path) -> Path:
    if ccf_file.name != "ccf.json":
        raise HTTPException(status_code=400, detail="不是一个 CCF 文件")

    if not ccf_file.exists():
        raise HTTPException(status_code=404, detail="CCF 文件不存在")

    if not ccf_file.is_file():
        raise HTTPException(status_code=400, detail="不是一个有效的文件")

    try:
        ccf = CCF.model_validate_json(ccf_file.read_text('utf-8'))
    except pydantic.ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"CCF 文件格式错误: {e.errors()}")

    return ccf_file


def require_ccf(ccf_file: Path = Depends(require_ccf_file)) -> CCF:
    return CCF.model_validate_json(ccf_file.read_text('utf-8'))


def require_oj_contest(contest_id: uuid.UUID) -> OJContest:
    query = Query()
    results = contestscol.search(query.contest_id == contest_id.__str__())

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="比赛不存在")

    return OJContest.model_validate(results[0])


def require_contest_started(contest: OJContest = Depends(require_oj_contest)) -> OJContest:
    if datetime.datetime.now().replace(tzinfo=None) < contest.start_time.replace(tzinfo=None):
        raise HTTPException(status_code=403, detail="比赛未开始")

    return contest
