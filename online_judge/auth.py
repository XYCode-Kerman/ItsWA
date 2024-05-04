import datetime
import os
from typing import *

import fastapi
import jwt
import pydantic
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import APIKeyCookie
from tinydb import Query

from .oj_models.user import User
from .utils import usercol

router = APIRouter(prefix='/auth', tags=['用户验证'])
apikey_schema = APIKeyCookie(name='itswa-oj-apikey')


def get_apikey_decoded(apikey: Optional[str] = Depends(apikey_schema)) -> Dict[Any, Any]:
    if not apikey:
        raise HTTPException(
            status_code=401, detail="请提供API Key")

    try:
        decoded = jwt.decode(
            apikey, key=os.environ['SECRET'], algorithms=['HS256'])
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="API Key无效")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="API Key已过期")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"未知错误: {e}")

    return decoded


def get_user(decoded: Dict[Any, Any] = Depends(get_apikey_decoded)) -> User:
    try:
        decoded = User(**decoded).model_dump()
    except pydantic.ValidationError:
        raise HTTPException(status_code=401, detail="API Key无效")

    User_Query = Query()
    result = usercol.search(User_Query.username == decoded['username'])[0]

    return User(**result)


def get_token(user: User) -> str:
    return jwt.encode(
        {
            **user.model_dump(mode='json'),
            'exp': datetime.datetime.now() + datetime.timedelta(days=7)
        },
        os.environ['SECRET']
    )


def require_role(roles: List[str] | str = ['default']) -> Callable[[User], User]:
    if isinstance(roles, str):
        roles = [roles]

    def wrapper(user: User = Depends(get_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="不符合权限要求")

        return user

    return wrapper


@router.post('/login', name='登录', responses={
    200: {
        "description": "登录成功",
        "content": {
            "application/json": {
                "example": {
                    'token': 'user_token'
                }
            }
        }
    }
})
async def user_login(username: Annotated[str, Body()], password: Annotated[str, Body()], response: fastapi.Response):
    User_Query = Query()
    results = usercol.search(User_Query.username ==
                             username and User_Query.password == password)

    if results.__len__() >= 1:
        token = get_token(User.model_validate(results[0]))
        response.set_cookie('itswa-oj-apikey', token,
                            expires=datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=7), httponly=True)

        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")


@router.post('/register', name='注册', response_model=User)
async def user_register(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    User_Query = Query()

    if usercol.search(User_Query.username == username).__len__() >= 1:
        raise HTTPException(status_code=409, detail="用户名已存在")

    usercol.insert(User(
        username=username,
        password=password,
        role='default'
    ).model_dump(mode='json'))

    return usercol.search(User_Query.username == username)[0]
