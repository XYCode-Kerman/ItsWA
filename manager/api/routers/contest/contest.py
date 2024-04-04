import json
import pathlib
import shutil
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ccf_parser import CCF, ContestIndex, ContestIndexList
from utils import init_contest

router = APIRouter(tags=['比赛管理'])


def autocreate_contest_file():
    Path('./config/contests.json').parent.mkdir(exist_ok=True, parents=True)

    if not Path('./config/contests.json').exists():
        Path('./config/contests.json').touch(exist_ok=True)
        Path('./config/contests.json').write_text('[]', 'utf-8')


@router.get('/', name='获取比赛列表', response_model=ContestIndexList)
async def get_contests():
    autocreate_contest_file()
    data: List[Dict[str, str]] = json.load(
        pathlib.Path('./config/contests.json').open())

    # 将ContestIndex中的 name、desc 与 CCF 同步
    for index, contest_index in enumerate(data):
        contest_index: ContestIndex = ContestIndex(**contest_index)

        if not contest_index.ccf_file.exists():
            del data[index]
        else:
            ccf = CCF(**json.loads(
                contest_index.ccf_file.joinpath('ccf.json').read_text('utf-8')
            ))

            data[index]['name'] = ccf.header.name
            data[index]['description'] = ccf.header.description

    json.dump(data, pathlib.Path('./config/contests.json').open('w'),
              indent=4, ensure_ascii=False)

    return [
        ContestIndex(**x)
        for x in data
    ]


@router.post('/', name='新建比赛', response_model=ContestIndex, description="""
> 注：path 是比赛目录而不是CCF文件位置。
""")
async def create_contest(path: pathlib.Path, ccf: CCF):
    autocreate_contest_file()
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


@router.delete('/', name='删除比赛', response_model=ContestIndex)
async def delete_contest(path: pathlib.Path):
    autocreate_contest_file()
    if not path.exists():
        raise HTTPException(status_code=404, detail='比赛目录不存在')

    if not path.joinpath('ccf.json').exists():
        raise HTTPException(status_code=404, detail='CCF文件不存在')

    indexes: List[Dict[str, str]] = json.load(
        pathlib.Path('./config/contests.json').open())

    results = [x for x in indexes if x['ccf_file']
               == path.absolute().__str__()]
    if results.__len__() == 0:
        raise HTTPException(status_code=404, detail='比赛目录不存在')
    else:
        shutil.rmtree(results[0]['ccf_file'], ignore_errors=True)
        indexes.remove(results[0])
        json.dump(indexes, pathlib.Path(
            './config/contests.json').open('w'), indent=4, ensure_ascii=False)

        return results[0]
