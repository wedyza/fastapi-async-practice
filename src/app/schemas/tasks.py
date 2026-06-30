from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from src.app.core.enums import TaskStatus, TaskType


class BaseTask(BaseModel):
    id: UUID
    task_name: str
    task_type: TaskType


class CreateTask(BaseModel):
    name: str
    task_type: TaskType
    urls: list[str] | None


class Task(BaseTask):
    user_id: UUID
    status: TaskStatus
    created_at: datetime
    result: dict[str, Any] | None = None
