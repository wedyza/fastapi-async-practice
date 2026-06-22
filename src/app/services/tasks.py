from uuid import UUID

from src.app.core.enums import TaskStatus, TaskType
from src.app.core.redis_settings import get_worker_client
from src.app.repositories.tasks import TaskRepository
from src.app.schemas.tasks import Task


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def list_tasks_by_user(self, user_id: UUID) -> list[Task]:
        tasks = await self._repository.list_tasks_by_user(user_id)
        return [
            Task(
                id=task.id,
                task_name=task.task_name,
                task_type=task.task_type,
                user_id=task.user_id,
                status=task.status,
                created_at=task.created_at
            ) for task in tasks
        ]

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
        queue = await get_worker_client()
        match task_type:
            case TaskType.ASLEEP:
                await queue.enqueue_job('asleep', _job_id=str(task.id))
            case _:
                ...
        return Task(
            id=task.id,
            task_name=task.task_name,
            task_type=task.task_type,
            user_id=task.user_id,
            status=task.status,
            created_at=task.created_at
        )

    async def update_task_status(self, task_id: UUID, task_status: TaskStatus):
        await self._repository.update_task_status(task_id, task_status)
