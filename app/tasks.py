from datetime import datetime, timedelta
from .celery import celery as app
from .utils import fetch_helper


@app.task
def fetch_data(start_time: datetime, end_time: datetime):
    print(f"Fetching data from {start_time} to {end_time}")
    result = fetch_helper(start_time, end_time)
    return {
        "status": "success",
        "start_time": start_time,
        "end_time": end_time,
        "result": result,
    }


@app.task
def scheduled_fetch_data():
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=30)
    start_time_str = start_time.isoformat()
    end_time_str = end_time.isoformat()
    fetch_data.delay(start_time_str, end_time_str)
