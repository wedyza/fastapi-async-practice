from uuid import UUID

from src.app.core.enums import TaskType
from src.app.repositories.tasks import TaskRepository
from src.app.schemas.tasks import Task


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def get_task_by_id(self, id: UUID):
        task = await self._repository.get_task_by_id(id)
        return Task(
            id=task.id,
            task_name=task.task_name,
            task_type=task.task_type,
            user_id=task.user_id,
            status=task.status,
            created_at=task.created_at
        )

    async def create_task(self, user_id: UUID, name: str, task_type: TaskType):
        task = await self._repository.create_task(user_id, name, task_type)
        # ЗАПУСК ТАСКИ В CELERY - ПОЛУЧЕНИЕ celery_task_id для получения информации о том, закончилась ли таска в celery_backend
        return Task(
            id=task.id,
            task_name=task.task_name,
            task_type=task.task_type,
            user_id=task.user_id,
            status=task.status,
            created_at=task.created_at
        )
