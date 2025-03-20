from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

def get_report(db: Session, id: int) -> Optional[Report]:
    return db.query(Report).filter(Report.id == id).first()

def get_employee_reports(
    db: Session, 
    employee_id: int,
    report_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Report]:
    query = db.query(Report).filter(Report.employee_id == employee_id)
    if report_type:
        query = query.filter(Report.report_type == report_type)
    if start_date:
        query = query.filter(Report.start_date >= start_date)
    if end_date:
        query = query.filter(Report.end_date <= end_date)
    return query.order_by(Report.created_at.desc()).all()

def create_report(db: Session, obj_in: ReportCreate) -> Report:
    db_report = Report(**obj_in.model_dump(), created_at=datetime.utcnow())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_report(
    db: Session, 
    db_obj: Report,
    obj_in: ReportUpdate
) -> Report:
    for key, value in obj_in.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_report(db: Session, id: int) -> bool:
    db_report = get_report(db, id)
    if db_report:
        db.delete(db_report)
        db.commit()
        return True
    return False 