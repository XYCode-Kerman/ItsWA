import json
import pathlib

from fastapi import APIRouter, HTTPException

from ccf_parser import CCF, ContestIndex, ContestIndexList
from utils import init_contest

router = APIRouter(tags=['比赛管理'])


@router.get('/', name='获取比赛列表', response_model=ContestIndexList)
async def get_contests():
    return [
        ContestIndex(**x)
        for x in json.load(pathlib.Path('./config/contests.json').open())
    ]


@router.post('/', name='新建比赛', response_model=ContestIndex, description="""
> 注：path 是比赛目录而不是CCF文件位置。
""")
async def create_contest(path: pathlib.Path, ccf: CCF):
    if path.exists() and path.joinpath('ccf.json').exists():
        raise HTTPException(status_code=400, detail='比赛目录已存在')
    path.mkdir(parents=True, exist_ok=True)

    init_contest(path, ccf)

    index = ContestIndex(
        name=ccf.header.name, description=ccf.header.description, ccf_file=path).model_dump()
    indexes = json.load(pathlib.Path('./config/contests.json').open())
    indexes.append(index)
    json.dump(
        [
            ContestIndex(**idx).model_dump(mode='json')
            for idx in indexes
        ],
        pathlib.Path(
            './config/contests.json').open('w'),
        indent=4,
        ensure_ascii=False
    )

    return index
