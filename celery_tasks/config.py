from celery import Celery

from core.config import settings

redis_celery_tasks_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_celery_broker_db}"
redis_celery_tasks_backend = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_celery_backend_db}"


celery = Celery('tasks', broker=redis_celery_tasks_url, backend=redis_celery_tasks_backend)
