from celery import Celery
from celery.schedules import crontab
from app.config import get_settings

settings = get_settings()

celery = Celery(
    __name__, broker=settings.celery_broker_url, backend=settings.celery_result_backend
)

celery.conf.beat_schedule = {
    "fetch-data-schedule": {
        "task": "app.tasks.scheduled_fetch_data",
        "schedule": crontab(minute="*/1"),
    },
}


celery.autodiscover_tasks(["app"])

celery.conf.update(
    task_routes={
        "app.tasks.*": {"queue": "celery"},
    },
    broker_connection_retry_on_startup=True,
)
