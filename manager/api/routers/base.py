import datetime

from fastapi import APIRouter

router = APIRouter(prefix='/base', tags=['基本'])


@router.get('/ping', responses={
    200: {
        'description': 'Ping 服务器，获取一些基本信息',
        'content': {
            'application/json': {
                'example': {'message': 'pong', 'server_time': '2024-03-25T23:39:25.899385'}
            }
        }
    }
})
async def ping():
    return {'message': 'pong', 'server_time': datetime.datetime.now().isoformat()}
