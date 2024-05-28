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
    # db = get_db()
    # start_time_dt = datetime.fromisoformat(start_time)
    # end_time_dt = datetime.fromisoformat(end_time)
    # sensor_data = db.query(SensorDataTable).filter(
    #     SensorDataTable.timestamp >= start_time_dt,
    #     SensorDataTable.timestamp <= end_time_dt
    # ).all()

    # return sensor_data

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


def group_data_by_sensor(data: List[SensorData]):
    grouped_data = defaultdict(list)

    for entry in data:
        sensor = entry["sensor"]
        timestamp = entry["timestamp"]
        value = entry["value"]

        grouped_data[sensor].append({"time": timestamp, "value": value})

    return dict(grouped_data)
