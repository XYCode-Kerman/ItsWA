import fastapi

from .routers import base_router

app = fastapi.FastAPI()
app.include_router(base_router)
