import requests
import logging
from datetime import datetime, timedelta
from .celery import celery as app
from .config import settings
from .utils import (
    fetch_helper,
    group_data_by_sensor,
    get_latest_run_time,
    update_latest_run_time,
)


@app.task
def fetch_data(start_time: datetime, end_time: datetime):
    logging.info(f"Fetching data from {start_time} to {end_time}")
    sensor_data = fetch_helper(start_time, end_time)
    task = post_data.delay(start_time, end_time, sensor_data)
    return {"task_id": task.id, "status": "success"}


@app.task
def scheduled_fetch_data():
    start_time = datetime.fromisoformat(get_latest_run_time())
    end_time = start_time + timedelta(minutes=settings.fetch_data_interval)
    fetch_data.delay(start_time, end_time)
    update_latest_run_time(end_time)
    return {"status": "success", "message": "Task scheduled"}


@app.task
def post_data(start_time: datetime, end_time: datetime, sensor_data):
    endpoint = settings.post_data_endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.post_data_api_key}",
    }

    # Apply data transformation here if needed
    grouped_data = group_data_by_sensor(sensor_data)
    payload = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "data": grouped_data,
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    return {"status": "success", "message": "Data posted successfully"}
