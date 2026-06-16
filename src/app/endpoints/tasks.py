from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.core.dependencies import auth_user, get_task_service
from src.app.core.enums import TaskType
from src.app.schemas import Task, User
from src.app.services.tasks import TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.post(path="", response_model=Task)
async def create_task(
    name: str,
    task_type: TaskType,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TaskService, Depends(get_task_service)]
):
    return await service.create_task(user.id, name, task_type)
