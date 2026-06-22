from typing import Any, Callable

from httpx import AsyncClient

from src.app.core.enums import TaskStatus
from src.app.core.redis_settings import redis_settings
from src.app.core.worker_dependencies import get_task_service, set_task_service
from src.app.repositories import TaskRepository
from src.app.services import TaskService
from src.app.tasks import TASKS


async def startup(ctx: dict[str, Any]):
    ctx['session'] = AsyncClient()
    set_task_service(TaskService(TaskRepository()))
    print('Successfuly started')

async def shutdown(ctx: dict[str, Any]):
    await ctx['session'].aclose()  # pyright: ignore[reportUnknownMemberType]
    # ctx['task_service'] = await get_task_service()
    print('End of the work')

async def on_task_start(ctx: dict[str, Any]):
    service = get_task_service()
    await service.update_task_status(ctx["job_id"], TaskStatus.IN_PROGRESS)

#on fail

async def on_task_end(ctx: dict[str, Any]):
    service = get_task_service()
    await service.update_task_status(ctx["job_id"], TaskStatus.FINISHED)

class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    functions: list[Callable[..., Any]] = TASKS
    on_job_start = on_task_start
    on_job_end = on_task_end
