from celery import Celery

from src.app.core.config import settings

celery_app = Celery(main="fastapi-async", broker=settings.REDIS_SETTINGS.REDIS_URL, backend=settings.REDIS_SETTINGS.REDIS_URL)

celery_app.autodiscover_tasks(packages=["app.tasks"])  # pyright: ignore[reportUnknownMemberType]
