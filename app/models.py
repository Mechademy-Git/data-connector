from pydantic import BaseModel
from datetime import datetime


class RequestTimeRange(BaseModel):
    start_time: datetime
    end_time: datetime


class AsyncTaskResult(BaseModel):
    task_id: str
    status: str
