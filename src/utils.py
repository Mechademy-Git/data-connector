from collections import defaultdict
from datetime import datetime
from typing import List
from .db import get_db
from .models import SensorDataTable, SensorData
from .schemas import SensorDataSchema
from sqlalchemy import text
from .query import construct_query
import pandas as pd


def fetch_helper(start_time: datetime, end_time: datetime) -> List[SensorData]:
    """
    Implement the logic to fetch data based on start_time and end_time
    For example, you might want to fetch data from a database or an external API
    """

    sql_query = construct_query()

    with get_db() as session:
        try:
            result = session.execute(text(sql_query))
            rows = result.fetchall()
            column_names = result.keys()
            df = pd.DataFrame(rows, column_names=column_names)
            json_result = df.to_json(orient="records")
            return json_result
        except Exception as e:
            print(f"An error occured: {e}")


def get_latest_run_time() -> datetime:
    """
    Implement the logic to get scheduler's last run time
    For example, you might want to fetch the last ran time from a database
    """

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
        sensor = entry["sensor_id"]
        timestamp = (
            entry["timestamp"].isoformat()
            if isinstance(entry["timestamp"], datetime)
            else entry["timestamp"]
        )
        value = entry["value"]

        grouped_data[sensor].append({"timestamp": timestamp, "value": value})

    return dict(grouped_data)
