import fastapi

from .routers import base_router, contest_router

app = fastapi.FastAPI()
app.include_router(base_router)
app.include_router(contest_router)
