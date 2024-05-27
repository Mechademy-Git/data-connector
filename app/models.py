from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


class RequestTimeRange(BaseModel):
    start_time: datetime
    end_time: datetime


class AsyncTaskResult(BaseModel):
    task_id: str
    status: str


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor = Column(String, index=True)
    value = Column(Integer)
    timestamp = Column(DateTime)
