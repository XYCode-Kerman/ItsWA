from pathlib import Path

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import base_router, contest_router

app = fastapi.FastAPI()
app.include_router(base_router)
app.include_router(contest_router)
app.mount("/editor", StaticFiles(directory=Path('./assets/ited').absolute(),
          html=True, check_dir=False))

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
