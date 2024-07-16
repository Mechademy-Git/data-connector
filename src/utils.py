from collections import defaultdict
from datetime import datetime
from typing import List
from .db import get_db
from .models import SensorDataTable, SensorData


def fetch_helper(start_time: str, end_time: str) -> List[SensorData]:
    """
    Implement the logic to fetch data based on start_time and end_time
    For example, you might want to fetch data from a database or an external API
    """

    # Example 1: Fetch data from a database
    # with get_db() as db:
    #     sensor_data = db.query(SensorDataTable).filter(
    #         SensorDataTable.timestamp >= start_time,
    #         SensorDataTable.timestamp <= end_time
    #     ).all()
    #     sensor_data = [SensorDataSchema.model_validate(data).model_dump() for data in sensor_data]
    #     return sensor_data

    # Remove hard-coded data below after implementing the logic to fetch data
    sensor_data = [
        {"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"},
        {"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:30"},
        {"sensor": "sensor_2", "value": 20, "timestamp": "2021-07-01T12:01:00"},
        {"sensor": "sensor_2", "value": 20, "timestamp": "2021-07-01T12:01:30"},
        {"sensor": "sensor_3", "value": 30, "timestamp": "2021-07-01T12:02:00"},
        {"sensor": "sensor_3", "value": 30, "timestamp": "2021-07-01T12:02:30"},
    ]
    return sensor_data


def get_latest_run_time() -> datetime:
    """
    Implement the logic to get scheduler's last run time
    For example, you might want to fetch the last ran time from a database
    """

    # Example 1: Fetch the last ran time from a database
    # db = get_db()
    # last_ran_time = db.query(LastRanTimeTable).first()

    # return last_ran_time

    # Remove hard-coded data below after implementing the logic to fetch the last ran time
    last_ran_time = "2021-07-01T12:00:00"
    return last_ran_time


def update_latest_run_time(timestamp: datetime):
    """
    Implement the logic to update scheduler's last run time
    For example, you might want to update the last ran time in a database
    """

    # Example 1: Update the last ran time in a database
    # db = get_db()
    # last_ran_time = db.query(LastRanTimeTable).first()
    # last_ran_time.timestamp = datetime.now()
    # db.commit()

    # Remove hard-coded data below after implementing the logic to update the last ran time
    pass


def group_data_by_sensor(data: List[SensorData]):
    grouped_data = defaultdict(list)

    for entry in data:
        sensor = entry["sensor"]
        timestamp = entry["timestamp"]
        value = entry["value"]

        grouped_data[sensor].append({"timestamp": timestamp, "value": value})

    return dict(grouped_data)
