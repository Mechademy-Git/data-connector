import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.tasks import fetch_data, scheduled_fetch_data, post_data
from src.config import settings


@patch("src.tasks.fetch_helper")
@patch("src.tasks.post_data.delay")
def test_fetch_data(mock_post_data_delay, mock_fetch_helper):
    mock_fetch_helper.return_value = [
        {"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"}
    ]
    task_id = "task_id"
    mock_post_data_delay.return_value = MagicMock(id=task_id)

    start_time = datetime(2021, 7, 1, 12, 0, 0)
    end_time = datetime(2021, 7, 1, 12, 30, 0)

    result = fetch_data(start_time, end_time)

    assert result == {"task_id": task_id, "status": "success"}
    mock_fetch_helper.assert_called_once_with(start_time, end_time)
    mock_post_data_delay.assert_called_once_with(
        start_time,
        end_time,
        [{"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"}],
    )


@patch("src.tasks.datetime")
@patch("src.tasks.get_latest_run_time")
@patch("src.tasks.update_latest_run_time")
@patch("src.tasks.fetch_data.delay")
def test_scheduled_fetch_data(
    mock_fetch_data_delay,
    mock_update_latest_run_time,
    mock_get_latest_run_time,
    mock_datetime,
):
    mock_get_latest_run_time.return_value = datetime(2021, 7, 1, 12, 0, 0).isoformat()
    mock_datetime.fromisoformat.side_effect = lambda x: datetime.fromisoformat(x)
    mock_datetime.utcnow.return_value = datetime(2021, 7, 1, 12, 30, 0)

    start_time = datetime(2021, 7, 1, 12, 0, 0)
    end_time = start_time + timedelta(minutes=settings.fetch_data_interval)
    result = scheduled_fetch_data()
    assert result == {"status": "success", "message": "Task scheduled"}
    mock_fetch_data_delay.assert_called_once_with(start_time, end_time)
    mock_update_latest_run_time.assert_called_once_with(end_time)


@patch("src.tasks.requests.post")
@patch("src.tasks.group_data_by_sensor")
def test_post_data(mock_group_data_by_sensor, mock_requests_post):
    mock_group_data_by_sensor.return_value = {
        "sensor_1": [{"timestamp": "2021-07-01T12:00:00", "value": 10}]
    }
    mock_requests_post.return_value.status_code = 200
    start_time = datetime(2021, 7, 1, 12, 0, 0)
    end_time = start_time + timedelta(minutes=settings.fetch_data_interval)
    sensor_data = [
        {"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"}
    ]
    result = post_data(start_time, end_time, sensor_data)
    assert result == {"status": "success", "message": "Data posted successfully"}
    mock_group_data_by_sensor.assert_called_once_with(sensor_data)
    mock_requests_post.assert_called_once_with(
        settings.post_data_endpoint,
        json={
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "data": {"sensor_1": [{"timestamp": "2021-07-01T12:00:00", "value": 10}]},
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.post_data_api_key}",
        },
    )
