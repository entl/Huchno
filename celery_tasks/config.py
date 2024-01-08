import asyncio

from celery import Celery

from core.config import settings

redis_celery_tasks_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_celery_db}"
redis_celery_tasks_backend = f"redis://{settings.redis_host}:{settings.redis_port}/1"


celery = Celery('tasks', broker=redis_celery_tasks_url, backend=redis_celery_tasks_backend)
