
from enum import Enum

from src.infrastructure.postgresql.models.task import TASKS_STATUSES, TASKS_TYPES

TaskType = Enum('TaskType', TASKS_TYPES)
TaskStatus = Enum('TaskStatus', TASKS_STATUSES)

# class TaskType(Enum):
#     ASLEEP = 'ASLEEP'
#     ASYNC_HTTP_REQUEST = "ASYNC HTTP REQUEST"
#     CELERY_TASK_PROCESSING = "CELERY TASK PROCESSING"
#     COROUTINE_LOG = "COROUTINE LOG"


# class TaskStatus(Enum):
#     CREATED = 'CREATED'
#     IN_PROGRESS = 'IN PROGRESS'
#     FINISHED = 'FINISHED'
