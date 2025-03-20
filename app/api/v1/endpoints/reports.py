from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas
from app.api import deps
from app.models.report import ReportType
from app.crud import (
    get_report,
    create_report,
    update_report,
    delete_report,
    get_employee_reports
)

router = APIRouter()

@router.get("/employee/{employee_id}", response_model=List[schemas.Report])
def read_employee_reports(
    employee_id: int,
    db: Session = Depends(deps.get_db),
    report_type: Optional[ReportType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Получить отчеты сотрудника.
    """
    reports = get_employee_reports(
        db, 
        employee_id=employee_id,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date
    )
    return reports

@router.post("/", response_model=schemas.Report)
def create_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    report_in: schemas.ReportCreate
):
    """
    Создать новый отчет.
    """
    report = create_report(db, obj_in=report_in)
    return report

@router.get("/{report_id}", response_model=schemas.Report)
def read_report_endpoint(
    report_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Получить информацию об отчете по ID.
    """
    report = get_report(db, id=report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Отчет не найден"
        )
    return report

@router.put("/{report_id}", response_model=schemas.Report)
def update_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    report_in: schemas.ReportUpdate
):
    """
    Обновить информацию об отчете.
    """
    report = get_report(db, id=report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Отчет не найден"
        )
    report = update_report(db, db_obj=report, obj_in=report_in)
    return report

@router.delete("/{report_id}")
def delete_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int
):
    """
    Удалить отчет.
    """
    report = get_report(db, id=report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Отчет не найден"
        )
    report = delete_report(db, id=report_id)
    return {"ok": True} 