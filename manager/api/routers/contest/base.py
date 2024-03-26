from fastapi import APIRouter

from .ccf import router as ccf_router
from .contest import router as contest_router

router = APIRouter(prefix='/contest')
router.include_router(ccf_router)
router.include_router(contest_router)
