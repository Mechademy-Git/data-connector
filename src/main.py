from fastapi import FastAPI, Depends, HTTPException
from src.auth import AuthBearer
from src.models import RequestTimeRange, AsyncTaskResult
from celery.result import AsyncResult
from .tasks import fetch_data, run_pipeline
from .celery import celery as celery_app


app = FastAPI()


@app.post("/raise-request", response_model=AsyncTaskResult)
async def raise_request(time_range: RequestTimeRange, _: str = Depends(AuthBearer())):
    try:
        task = run_pipeline.delay(time_range.start_time, time_range.end_time)
        return {"task_id": task.id, "status": "task submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str, _: str = Depends(AuthBearer())):
    task = AsyncResult(task_id, app=celery_app)
    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return response


app.mount("/api/v1", app)
