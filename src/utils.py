from collections import defaultdict
from datetime import datetime
from typing import List
from .db import get_db
from .models import SensorDataTable, SensorData
from .schemas import SensorDataSchema
from sqlalchemy import text
from .query import construct_query
import pandas as pd
import os
import json


def fetch_helper(start_time: datetime, end_time: datetime) -> List[SensorData]:
    """
    Implement the logic to fetch data based on start_time and end_time
    For example, you might want to fetch data from a database or an external API
    """

    sql_query = construct_query(start_time, end_time)

    with get_db() as session:
        try:
            result = session.execute(sql_query, {'start': start_time, 'end': end_time})
            rows = result.fetchall()
            column_names = result.keys()
            df = pd.DataFrame(rows, columns=column_names)
            print(df.head())
            json_result = df.to_json(orient="records")
            return json.loads(json_result)
        except Exception as e:
            print(f"An error occured: {e}")

def get_latest_run_time() -> datetime:
    """
    Implement the logic to get scheduler's last run time
    For example, you might want to fetch the last ran time from a database
    """
    try:
        # Get the current working directory
        current_dir = os.getcwd()
        
        # Define the target directory
        target_dir = os.path.join(current_dir, 'loads')
        
        # Ensure the target directory exists
        if not os.path.exists(target_dir):
            print(f"The directory '{target_dir}' does not exist.")
            return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")
        
        # List all files in the target directory
        files = os.listdir(target_dir)
        
        # Filter out files that don't match the pattern 'run_{timestamp}.DONE'
        run_files = [f for f in files if f.startswith('run_') and f.endswith('.DONE')]
        
        if not run_files:
            print("No valid run files found in the directory.")
            return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")
        
        # Extract timestamps and convert them to datetime objects
        timestamps = []
        for file in run_files:
            timestamp_str = file[4:-5]  # Extract the part after 'run_' and before '.DONE'
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                timestamps.append(timestamp)
            except ValueError:
                print(f"Skipping file with invalid timestamp format: {file}")
        
        if not timestamps:
            print("No valid timestamps found in the run files.")
            return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")
        
        # Get the most recent timestamp
        latest_timestamp = max(timestamps)
        
        return latest_timestamp
    
    except Exception as e:
        print(f"Error fetching the latest run time: {e}")
        return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")
    
    except Exception as e:
        print(f"Error fetching the latest run time: {e}")
        return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")
    
    except Exception as e:
        print(f"Error fetching the latest run time: {e}")
        return datetime.strptime("1970-01-01_00-00-00", "%Y-%m-%d_%H-%M-%S")

def update_latest_run_time(timestamp: datetime):
    """
    Implement the logic to update scheduler's last run time
    For example, you might want to update the last ran time in a database
    """
    try:
        # Convert the timestamp to the desired format
        formatted_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Get the current working directory
        current_dir = os.getcwd()
        
        # Define the target directory
        target_dir = os.path.join(current_dir, 'loads')
        
        # Ensure the target directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        # Create the filename
        filename = f"run_{formatted_timestamp}.DONE"
        
        # Create the full file path
        file_path = os.path.join(target_dir, filename)
        
        # Create the file
        with open(file_path, 'w') as file:
            pass
        
        print(f"File '{filename}' created successfully in '{target_dir}'")
    
    except Exception as e:
        print(f"Error creating file: {e}")

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
