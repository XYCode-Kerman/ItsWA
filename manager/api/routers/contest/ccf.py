import datetime
import json
import pathlib

import pydantic
from fastapi import APIRouter, HTTPException, Response

from ccf_parser import CCF

router = APIRouter(prefix='/ccf', tags=['CCF 文件管理'])


@router.get('/', response_model=CCF, name='获取 CCF 文件')
async def get_ccf(path: pathlib.Path):
    if not path.exists():
        raise HTTPException(status_code=404, detail='文件不存在')

    if not path.name == 'ccf.json':
        raise HTTPException(status_code=400, detail='文件名不是 ccf.json')

    try:
        ccf = CCF(
            **json.loads(path.read_text(encoding='utf-8'))
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='JSON 格式错误')
    except (pydantic.ValidationError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ccf


@router.put('/', response_model=CCF, name='更新 CCF 文件')
async def update_ccf(path: pathlib.Path, ccf: CCF):
    if not path.exists():
        raise HTTPException(status_code=404, detail='文件不存在')

    if not path.name == 'ccf.json':
        raise HTTPException(status_code=400, detail='文件名不是 ccf.json')

    path.write_text(ccf.model_dump_json(indent=4), encoding='utf-8')

    return ccf
