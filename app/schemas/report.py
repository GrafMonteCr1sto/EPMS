from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
from app.models.report import ReportType

class ReportBase(BaseModel):
    employee_id: int
    report_type: ReportType
    start_date: datetime
    end_date: datetime
    data: Dict[str, Any]

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 