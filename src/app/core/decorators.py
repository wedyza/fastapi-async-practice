from typing import Annotated, Any, Callable

from arq.connections import ArqRedis
from fastapi import Depends

from src.app.core.config import settings
from src.app.core.dependencies import get_worker


def async_picker(func:Callable[..., Any]) -> Callable[..., Any]:
    async def wrapper(worker: Annotated[ArqRedis, Depends(get_worker)], *args, **kwargs):
        if settings.LAUNCHED_IN_CONTAINER:
            await worker.enqueue_job(func.__name__, args)  # pyright: ignore[reportFunctionMemberAccess]
        return await func(*args, **kwargs)
    return wrapper  # pyright: ignore[reportUnknownVariableType]
