from fastapi import APIRouter

from .judge import router as judge_router
from .manager import router as manager_router
from .problems import router as problems_router

router = APIRouter(prefix='/contests', tags=['比赛'])
router.include_router(manager_router)
router.include_router(problems_router)
router.include_router(judge_router)
