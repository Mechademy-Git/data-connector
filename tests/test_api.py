import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.config import settings

client = TestClient(fastapi_app)


@pytest.fixture
def mock_api_key():
    return settings.api_key


def test_raise_request(mocker, mock_api_key):
    mocker.patch("app.auth.AuthBearer.__call__", return_value=mock_api_key)
    mocker.patch("app.tasks.fetch_data.delay", return_value=mocker.Mock(id="task_id"))

    response = client.post(
        "/api/v1/raise-request",
        json={"start_time": "2021-07-01T12:00:00", "end_time": "2021-07-01T12:30:00"},
        headers={"Authorization": f"Bearer {mock_api_key}"},
    )

    assert response.status_code == 200
    assert response.json() == {"task_id": "task_id", "status": "task submitted"}


def test_get_task_status_pending(mocker, mock_api_key):
    mocker.patch("app.auth.AuthBearer.__call__", return_value=mock_api_key)
    mock_async_result = mocker.Mock(state="PENDING", info={})
    mocker.patch("app.main.AsyncResult", return_value=mock_async_result)

    response = client.get(
        "/api/v1/tasks/task_id", headers={"Authorization": f"Bearer {mock_api_key}"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "state": "PENDING",
        "current": 0,
        "total": 1,
        "status": "Pending...",
    }
