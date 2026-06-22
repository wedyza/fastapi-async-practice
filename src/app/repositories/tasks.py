from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select, update

from src.app.core.enums import TaskStatus, TaskType
from src.app.core.exceptions import NotFoundException
from src.infrastructure.postgresql.db_engine import async_session_factory
from src.infrastructure.postgresql.models import TasksOrm


@dataclass(slots=True, frozen=True)
class TaskRecord:
    id: UUID
    task_name: str
    user_id: UUID
    task_type: TaskType
    status: TaskStatus
    created_at: datetime

class TaskRepository:
    async def list_tasks_by_user(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[TaskRecord]:
        async with async_session_factory() as session:
            query = (
                select(
                    TasksOrm.id,
                    TasksOrm.task_name,
                    TasksOrm.user_id,
                    TasksOrm.task_type,
                    TasksOrm.status,
                    TasksOrm.created_at
                )
                .where(TasksOrm.user_id == user_id)
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            row = result.all()
            if len(row) == 0:
                return []
            tasks = [
                TaskRecord(
                    id=task_id,
                    task_name=task_name,
                    user_id=task_user_id,
                    task_type=task_type,
                    status=status,
                    created_at=created_at
                ) for task_id, task_name, task_user_id, task_type, status, created_at in row
            ]
            return tasks

    async def get_task_by_id(self, id: UUID) -> TaskRecord:
        async with async_session_factory() as session:
            query = (
                select(
                    TasksOrm.id,
                    TasksOrm.task_name,
                    TasksOrm.user_id,
                    TasksOrm.task_type,
                    TasksOrm.status,
                    TasksOrm.created_at
                )
                .where(TasksOrm.id == id)
                .limit(1)
            )
            result = await session.execute(query)
            row = result.one_or_none()
            if row is None:
                raise NotFoundException(f"Task с id={id} не найдена!")
            task_id, task_name, task_user_id, task_type, status, created_at = row
            return TaskRecord(
                id=task_id,
                task_name=task_name,
                user_id=task_user_id,
                task_type=task_type,
                status=status,
                created_at=created_at
            )

    async def create_task(self, user_id: UUID, name: str, task_type: TaskType):
        async with async_session_factory() as session:
            created_task = TasksOrm(
                id=uuid4(),
                task_name=name,
                user_id=user_id,
                task_type=task_type.value,
                status='CREATED'
            )
            session.add(created_task)
            await session.commit()
            return TaskRecord(
                id=created_task.id,
                task_name=created_task.task_name,
                user_id=created_task.user_id,
                task_type=TaskType(created_task.task_type),
                status=TaskStatus(created_task.status),
                created_at=created_task.created_at
            )

    async def update_task_status(self, task_id: UUID, task_status: TaskStatus):
        async with async_session_factory() as session:
            query = (
                update(TasksOrm)
                .where(TasksOrm.id == task_id)
                .values(status=task_status.value)
                .returning(TasksOrm.id)
            )
            update_result = await session.execute(query)
            updated_task_id = update_result.scalar_one_or_none()
            if updated_task_id is None:
                raise NotFoundException(f"Таска с таким id={task_id} не найден!")
            await session.commit()
