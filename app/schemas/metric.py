from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.metric import MetricType

class MetricBase(BaseModel):
    employee_id: int
    metric_type: MetricType
    value: float
    date: datetime
    description: Optional[str] = None

class MetricCreate(MetricBase):
    pass

class MetricUpdate(MetricBase):
    pass

class Metric(MetricBase):
    id: int

    class Config:
        from_attributes = True 