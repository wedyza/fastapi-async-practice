
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.core.exceptions import CustomExceptionBase
from src.app.core.exceptions_handlers import custom_exception_handler
from src.app.core.redis_settings import (
    close_redis_client,
    close_worker_client,
    init_redis_client,
    init_worker_client,
)
from src.app.endpoints import create_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_worker_client()
    await init_redis_client()
    yield
    await close_redis_client()
    await close_worker_client()

def create_app() -> FastAPI:
    app = FastAPI(
        title="test web",
        version="0.1.0",
        lifespan=lifespan
    )
    app.add_exception_handler(CustomExceptionBase, custom_exception_handler)
    app.include_router(create_api_router())
    return app


app = create_app()
