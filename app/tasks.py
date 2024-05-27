import requests
import logging
from datetime import datetime, timedelta
from .celery import celery as app
from .config import settings
from .utils import fetch_helper


@app.task
def fetch_data(start_time: datetime, end_time: datetime):
    logging.info(f"Fetching data from {start_time} to {end_time}")
    sensor_data = fetch_helper(start_time, end_time)
    post_data_to_endpoint.delay(sensor_data)


@app.task
def scheduled_fetch_data():
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=30)
    start_time_str = start_time.isoformat()
    end_time_str = end_time.isoformat()
    logging.info(f"Fetching data from {start_time} to {end_time}")
    sensor_data = fetch_helper(start_time_str, end_time_str)
    post_data_to_endpoint.delay(sensor_data)


@app.task
def post_data_to_endpoint(sensor_data):
    endpoint = settings.post_data_endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.post_data_api_key}",
    }
    payload = [
        {
            "sensor": data.sensor,
            "value": data.value,
            "timestamp": data.timestamp.isoformat(),
        }
        for data in sensor_data
    ]
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    return {"status": "success", "message": "Data posted successfully"}
