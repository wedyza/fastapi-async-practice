from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router


def create_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(auth_router)
    router.include_router(users_router)
    return router
