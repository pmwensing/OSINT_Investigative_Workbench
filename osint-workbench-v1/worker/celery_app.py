from celery import Celery
from api.core.config import settings

celery_app = Celery("osint_workbench", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_routes = {"worker.tasks.run_job": {"queue": "osint"}}
