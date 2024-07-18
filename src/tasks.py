import dlt
import logging
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from datetime import datetime, timedelta
from .celery import celery as app
from .config import settings
from .utils import (
    fetch_helper,
    get_latest_run_time,
    update_latest_run_time,
)

@dlt.resource()
def fetch_data(start_time: datetime, end_time: datetime):
    """
    Fetch sensor data for the given time range.
    
    Args:
        start_time (datetime): Start of the time range.
        end_time (datetime): End of the time range.
    
    Yields:
        dict: Sensor data entries.
    """
    logging.info(f"Fetching data from {start_time} to {end_time}")
    sensor_data = fetch_helper(start_time, end_time)
    for data in sensor_data:
        yield {**data}

# Optional transformer for manipulating data pre-load
# Lots of flexibility. Can read and write using pandas, can enforce schema if needed, can also simply return instead of yield.
# Uncomment if needed
# @dlt.transformer(data_from=fetch_data)
# def transform_data(data):
#     for item in data:
#         yield item

@dlt.destination(batch_size=10)
def post_data(data, schema):
    """
    Post data to the API endpoint.
    
    Args:
        data (dict): Data to be posted.
        schema (dict): Schema of the data.
    
    Returns:
        dict: Status of the post operation.
    """
    headers = {
        "Content-Type": "application/json",
    }
    client = RESTClient(
        base_url=settings.api_base_url,
        headers=headers,
        auth=BearerTokenAuth(token=settings.post_data_api_key)
    )
    response = client.post(path=settings.api_post_endpoint, json=data)
    response.raise_for_status()
    return {"status": "success", "message": "Data posted successfully"}

@app.task(bind=True)
def run_pipeline(self, start_time: datetime, end_time: datetime):
    """
    Run the data pipeline to fetch and post data.
    
    Args:
        self: Task instance (provided by Celery).
        start_time (datetime): Start of the time range.
        end_time (datetime): End of the time range.
    
    Returns:
        dict: Status and details of the pipeline execution.
    """
    try:
        pipeline = dlt.pipeline(
            pipeline_name="sensor_data_pipeline",
            destination=post_data,
            dataset_name="sensor_data"
        )
        
        info = pipeline.run(
            fetch_data(start_time, end_time),
            loader_file_format='j'
        )
        update_latest_run_time(end_time)
        return {
            "status": "success",
            "message": "Pipeline executed successfully",
            "details": info.dict()
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise

@app.task
def scheduled_run_pipeline():
    """
    Scheduled task to run the pipeline for the next time interval.
    
    Returns:
        dict: Task ID and status of the scheduled run.
    """
    start_time = datetime.fromisoformat(get_latest_run_time())
    end_time = start_time + timedelta(minutes=settings.fetch_data_interval)
    task = run_pipeline.delay(start_time, end_time)
    
    return {"task_id": task.id, "status": "Task scheduled"}