from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.employee import Department, Position

class EmployeeBase(BaseModel):
    full_name: str
    email: str
    position: Position
    department: Department
    hire_date: datetime
    salary: float
    manager_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[Position] = None
    department: Optional[Department] = None
    hire_date: Optional[datetime] = None
    salary: Optional[float] = None
    manager_id: Optional[int] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True 