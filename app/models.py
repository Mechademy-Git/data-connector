from typing import Optional, Union
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


class SensorData(BaseModel):
    sensor: str
    value: Union[int, float, str, None]
    timestamp: datetime


class SensorDataTable(Base):
    """Update the class definition to match the database schema"""

    # Example: If the database schema is as follows:

    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor = Column(String, index=True)
    value = Column(Integer)
    timestamp = Column(DateTime)
