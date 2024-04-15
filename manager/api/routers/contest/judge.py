import json
import uuid
from pathlib import Path
from typing import *

import fastapi
from fastapi import APIRouter, BackgroundTasks, FastAPI

import ccf_parser
import judge

router = APIRouter(prefix='/judge', tags=['评测管理'])
trackIds2Results: Dict[uuid.UUID, List[ccf_parser.JudgingResult]] = {}
judging: List[uuid.UUID] = []


def start_judging_task(ccf: ccf_parser.CCF, trackId: uuid.UUID):
    # trackIds2Results[trackId] = judge.start_judging(ccf)
    trackIds2Results[trackId] = []
    judging.append(trackId)
    for result in judge.start_judging(ccf):
        trackIds2Results[trackId].append(result)
        trackIds2Results[trackId].sort(key=lambda x: x.player_order)
    judging.remove(trackId)


@router.post('/start', name='开始评测', response_model=Dict[str, str], responses={
    200: {
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'trackId': {
                            'type': 'string'
                        }
                    }
                },
                'example': {
                    'trackId': '114514-1919810-114514-1919810-1919810'
                }
            }
        }
    }
})
async def start_judge(contest_path: Path, background_tasks: BackgroundTasks):
    if not contest_path.exists():
        raise fastapi.HTTPException(status_code=404, detail='路径不存在')

    if not contest_path.joinpath('ccf.json').exists():
        raise fastapi.HTTPException(status_code=404, detail='ccf.json 文件不存在')

    ccf_file = contest_path.joinpath('ccf.json')
    ccf = ccf_parser.CCF.model_validate_json(ccf_file.read_text('utf-8'))

    trackId = uuid.uuid4()
    background_tasks.add_task(start_judging_task, ccf, trackId)

    return {
        'trackId': trackId.__str__()
    }


@router.get('/result/{trackId}', name='获取评测结果', response_model=List[ccf_parser.JudgingResult])
async def get_judging_result(trackId: uuid.UUID):
    if trackIds2Results.get(trackId, None) is None:
        raise fastapi.HTTPException(status_code=404, detail='trackId 不存在')

    return trackIds2Results[trackId]


@router.get('/is_judging/{trackId}', name='获取某个比赛是否处于评测状态', response_model=bool)
async def get_contest_is_judging(trackId: uuid.UUID):  # pragma: no cover
    return trackId in judging
