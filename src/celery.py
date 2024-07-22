from celery import Celery
from celery.schedules import crontab
from src.config import settings


celery = Celery(
    __name__, broker=settings.celery_broker_url, backend=settings.celery_result_backend
)

celery.conf.beat_schedule = {
    "fetch-data-schedule": {
        "task": "src.tasks.scheduled_run_pipeline",
        "schedule": crontab(minute=f"*/{settings.fetch_data_interval}"),
    },
}


celery.autodiscover_tasks(["src"])

celery.conf.update(
    task_default_retry_delay=60,
    task_annotations={"*": {"max_retries": 10}},
    task_routes={
        "src.tasks.*": {"queue": "celery"},
    },
    broker_connection_retry_on_startup=True,
)
