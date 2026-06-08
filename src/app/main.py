
from fastapi import FastAPI

from src.app.endpoints import create_api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="test web",
        version="0.1.0",
    )
    app.include_router(create_api_router())
    return app


app = create_app()
