from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class ReportType(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    report_type = Column(Enum(ReportType))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    data = Column(JSON)
    created_at = Column(DateTime)
    
    # Отношения
    employee = relationship("Employee", back_populates="reports") 