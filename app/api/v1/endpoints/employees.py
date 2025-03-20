from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.models.employee import Department

router = APIRouter()

@router.get("/", response_model=List[schemas.Employee])
def read_employees(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    department: Optional[Department] = None
):
    """
    Получить список сотрудников.
    """
    employees = crud.get_employees(
        db, skip=skip, limit=limit
    )
    return employees

@router.post("/", response_model=schemas.Employee)
def create_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_in: schemas.EmployeeCreate
):
    """
    Создать нового сотрудника.
    """
    employee = crud.get_employee_by_email(db, email=employee_in.email)
    if employee:
        raise HTTPException(
            status_code=400,
            detail="Сотрудник с таким email уже существует."
        )
    employee = crud.create_employee(db, obj_in=employee_in)
    return employee

@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(
    employee_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Получить информацию о сотруднике по ID.
    """
    employee = crud.get_employee(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Сотрудник не найден"
        )
    return employee

@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int,
    employee_in: schemas.EmployeeUpdate
):
    """
    Обновить информацию о сотруднике.
    """
    employee = crud.get_employee(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Сотрудник не найден"
        )
    employee = crud.update_employee(db, db_obj=employee, obj_in=employee_in)
    return employee

@router.delete("/{employee_id}")
def delete_employee(
    *,
    db: Session = Depends(deps.get_db),
    employee_id: int
):
    """
    Удалить сотрудника.
    """
    employee = crud.get_employee(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Сотрудник не найден"
        )
    employee = crud.delete_employee(db, id=employee_id)
    return {"ok": True} 