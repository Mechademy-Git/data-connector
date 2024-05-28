import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.tasks import fetch_data, scheduled_fetch_data, post_data
from app.config import settings


@patch("app.tasks.fetch_helper")
@patch("app.tasks.post_data.delay")
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
        [{"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"}]
    )


@patch("app.tasks.datetime")
@patch("app.tasks.get_latest_run_time")
@patch("app.tasks.update_latest_run_time")
@patch("app.tasks.fetch_data.delay")
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


@patch("app.tasks.requests.post")
@patch("app.tasks.group_data_by_sensor")
def test_post_data(mock_group_data_by_sensor, mock_requests_post):
    mock_group_data_by_sensor.return_value = {
        "sensor_1": [{"time": "2021-07-01T12:00:00", "value": 10}]
    }
    mock_requests_post.return_value.status_code = 200
    sensor_data = [
        {"sensor": "sensor_1", "value": 10, "timestamp": "2021-07-01T12:00:00"}
    ]
    result = post_data(sensor_data)
    assert result == {"status": "success", "message": "Data posted successfully"}
    mock_group_data_by_sensor.assert_called_once_with(sensor_data)
    mock_requests_post.assert_called_once_with(
        settings.post_data_endpoint,
        json={"sensor_1": [{"time": "2021-07-01T12:00:00", "value": 10}]},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.post_data_api_key}",
        },
    )
