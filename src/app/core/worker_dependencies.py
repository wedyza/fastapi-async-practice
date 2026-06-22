from typing import Optional

from src.app.services import TaskService

_task_service: Optional[TaskService] = None

def set_task_service(service: TaskService) -> None:
    global _task_service
    _task_service = service

def get_task_service() -> TaskService:
    if _task_service is None:
        raise RuntimeError("TaskService not initialized")
    return _task_service
