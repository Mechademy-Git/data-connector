from pydantic import BaseModel
from datetime import datetime


class SensorDataBaseSchema(BaseModel):
    sensor_id: int
    value: float
    timestamp: datetime


class SensorDataCreateSchema(SensorDataBaseSchema):
    pass


class SensorDataSchema(SensorDataBaseSchema):
    id: int

    class Config:
        from_attributes = True
