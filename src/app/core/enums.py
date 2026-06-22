
from enum import Enum

# TaskType = StrEnum('TaskType', {v: v for v in TASKS_TYPES})
# TaskStatus = StrEnum('TaskStatus', {v: v for v in TASKS_STATUSES})

class TaskType(Enum):
    ASLEEP = 'ASLEEP'
    ASYNC_HTTP_REQUEST = "ASYNC HTTP REQUEST"
    CELERY_TASK_PROCESSING = "CELERY TASK PROCESSING"
    COROUTINE_LOG = "COROUTINE LOG"


class TaskStatus(Enum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN PROGRESS'
    FINISHED = 'FINISHED'
