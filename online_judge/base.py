import multiprocessing

import fastapi
import uvicorn

from utils import online_judge_logger as logger

from .auth import router as auth_router
from .contests import router as contests_router

app = fastapi.FastAPI(title='ItsWA Online Judge API')
app.include_router(contests_router)
app.include_router(auth_router)


def _start_oj():  # proagma: no cover
    logger.info('Online Judge API 启动, 地址 http://0.0.0.0:6572/')
    uvicorn.run('online_judge:oj_app', host="0.0.0.0", port=6572,
                workers=6, log_level='info')


def start_oj_background():  # pragma: no cover
    process = multiprocessing.Process(target=_start_oj)
    process.start()

    return process
