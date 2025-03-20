from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricUpdate

def get_metric(db: Session, id: int) -> Optional[Metric]:
    return db.query(Metric).filter(Metric.id == id).first()

def get_employee_metrics(
    db: Session, 
    employee_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Metric]:
    query = db.query(Metric).filter(Metric.employee_id == employee_id)
    if start_date:
        query = query.filter(Metric.date >= start_date)
    if end_date:
        query = query.filter(Metric.date <= end_date)
    return query.order_by(Metric.date.desc()).all()

def create_metric(db: Session, obj_in: MetricCreate) -> Metric:
    db_metric = Metric(**obj_in.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def update_metric(
    db: Session, 
    db_obj: Metric,
    obj_in: MetricUpdate
) -> Optional[Metric]:
    for key, value in obj_in.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_metric(db: Session, id: int) -> bool:
    db_metric = get_metric(db, id)
    if db_metric:
        db.delete(db_metric)
        db.commit()
        return True
    return False 