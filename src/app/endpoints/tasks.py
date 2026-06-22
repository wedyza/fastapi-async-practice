from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket

from src.app.core.connect_manager import ConnectManager
from src.app.core.dependencies import auth_user, get_connect_manager, get_task_service
from src.app.core.enums import TaskType
from src.app.schemas import Task, User
from src.app.services.tasks import TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get(path="", response_model=list[Task])
async def list_tasks(
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TaskService, Depends(get_task_service)]
):
    return await service.list_tasks_by_user(user.id)

@router.post(path="", response_model=Task)
async def create_task(
    name: str,
    task_type: TaskType,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TaskService, Depends(get_task_service)]
):
    return await service.create_task(user.id, name, task_type)

@router.websocket(path="/ws", name="tasks-connect-ws")
async def tasks_ws(
    websocket: WebSocket,
    connect_manager: Annotated[ConnectManager, Depends(get_connect_manager)],
    user: Annotated[User, Depends(auth_user)]
):
    await connect_manager.connect(user.id, websocket)
