from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgresql.models.base import Base

TASKS_TYPES: tuple[str, ...] = (
    "ASLEEP",
    "ASYNC HTTP REQUEST",
    "CELERY TASK PROCESSING",
    "COROUTINE LOG"
)

TASKS_STATUSES = (
    'CREATED',
    'IN PROGRESS',
    'FINISHED'
)

def _task_type_check(column_name: str, constraint_name: str) -> CheckConstraint:
    allowed_values = ", ".join(repr(value) for value in TASKS_TYPES) # repr, чтобы обрамить слово в кавычки repr("string") = "string"
    return CheckConstraint(
        f"{column_name} IN ({allowed_values})",
        name=constraint_name
    )

class TasksOrm(Base):
    __tablename__: str = "tasks"
    __table_args__ = (  # pyright: ignore[reportAny, reportUnannotatedClassAttribute]
        _task_type_check("task_type", "tasks_type_check"),
        UniqueConstraint(
            "user_id",
            "local_index",
            name="tasks_user_id_local_index_unique"
        )
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    task_name: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", name="tasks_users_id_foreign"),
        primary_key=True
    )
    task_type: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
