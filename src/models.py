from typing import Union
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
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


class BookMarksTable(Base):
    """Update the class definition to match the database schema"""

    # Example: If the database schema is as follows:

    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    timestamp = Column(DateTime)


class SensorDataTable(Base):
    """Update the class definition to match the database schema"""

    # Example: If the database schema is as follows:

    __tablename__ = "core_sensordata"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, index=True)
    value = Column(Float)
    timestamp = Column(DateTime)
    