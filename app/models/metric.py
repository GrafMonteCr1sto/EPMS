from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class MetricType(str, enum.Enum):
    PRODUCTIVITY = "productivity"
    QUALITY = "quality"
    EFFICIENCY = "efficiency"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    LEADERSHIP = "leadership"

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    metric_type = Column(Enum(MetricType))
    value = Column(Float)
    date = Column(DateTime)
    description = Column(String, nullable=True)
    
    # Отношения
    employee = relationship("Employee", back_populates="metrics") 