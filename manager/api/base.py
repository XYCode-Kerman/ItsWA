import fastapi
from fastapi.middleware.cors import CORSMiddleware

from .routers import base_router, contest_router

app = fastapi.FastAPI()
app.include_router(base_router)
app.include_router(contest_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
