from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import schemas
from app.api import deps
from app.crud import (
    get_metric,
    create_metric,
    update_metric,
    delete_metric,
    get_employee_metrics
)

router = APIRouter()

@router.get("/employee/{employee_id}", response_model=List[schemas.Metric])
def read_employee_metrics(
    employee_id: int,
    db: Session = Depends(deps.get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Получить метрики сотрудника.
    """
    metrics = get_employee_metrics(
        db, employee_id=employee_id, start_date=start_date, end_date=end_date
    )
    return metrics

@router.post("/", response_model=schemas.Metric)
def create_metric_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    metric_in: schemas.MetricCreate
):
    """
    Создать новую метрику.
    """
    metric = create_metric(db, obj_in=metric_in)
    return metric

@router.get("/{metric_id}", response_model=schemas.Metric)
def read_metric_endpoint(
    metric_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Получить информацию о метрике по ID.
    """
    metric = get_metric(db, id=metric_id)
    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Метрика не найдена"
        )
    return metric

@router.put("/{metric_id}", response_model=schemas.Metric)
def update_metric_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    metric_id: int,
    metric_in: schemas.MetricUpdate
):
    """
    Обновить информацию о метрике.
    """
    metric = get_metric(db, id=metric_id)
    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Метрика не найдена"
        )
    metric = update_metric(db, db_obj=metric, obj_in=metric_in)
    return metric

@router.delete("/{metric_id}")
def delete_metric_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    metric_id: int
):
    """
    Удалить метрику.
    """
    metric = get_metric(db, id=metric_id)
    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Метрика не найдена"
        )
    metric = delete_metric(db, id=metric_id)
    return {"ok": True} 