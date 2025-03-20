from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def get_employee(db: Session, id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == id).first()

def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.email == email).first()

def get_employees(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, obj_in: EmployeeCreate) -> Employee:
    db_employee = Employee(
        full_name=obj_in.full_name,
        email=obj_in.email,
        position=obj_in.position,
        department=obj_in.department,
        hire_date=obj_in.hire_date,
        salary=obj_in.salary,
        manager_id=obj_in.manager_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(
    db: Session,
    db_obj: Employee,
    obj_in: EmployeeUpdate
) -> Employee:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_employee(db: Session, id: int) -> bool:
    db_employee = get_employee(db, id)
    if not db_employee:
        return False
    
    db.delete(db_employee)
    db.commit()
    return True 