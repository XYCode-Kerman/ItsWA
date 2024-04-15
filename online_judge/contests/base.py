from fastapi import APIRouter

from .manager import router as manager_router

router = APIRouter(prefix='/contests', tags=['比赛'])
router.include_router(manager_router)
