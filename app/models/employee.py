from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class Department(str, enum.Enum):
    IT = "IT"
    HR = "HR"
    SALES = "Sales"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    OPERATIONS = "Operations"

class Position(str, enum.Enum):
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"
    MANAGER = "Manager"
    DIRECTOR = "Director"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    position = Column(String)
    department = Column(String)
    hire_date = Column(DateTime)
    salary = Column(Float)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Отношения
    manager = relationship("Employee", remote_side=[id], backref="subordinates")
    metrics = relationship("Metric", back_populates="employee")
    reports = relationship("Report", back_populates="employee") 