from app.worker import celery_app
from app import crud
from app.db.session import SessionLocal
from datetime import datetime, timedelta
import pandas as pd
import json

@celery_app.task
def generate_daily_report():
    """
    Генерация ежедневного отчета по эффективности сотрудников
    """
    db = SessionLocal()
    try:
        # Получаем всех сотрудников
        employees = crud.employee.get_employees(db)
        
        for employee in employees:
            # Получаем метрики за последние 24 часа
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=1)
            
            metrics = crud.metric.get_employee_metrics(
                db, 
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Анализируем метрики
            metrics_data = []
            for metric in metrics:
                metrics_data.append({
                    "type": metric.metric_type,
                    "value": metric.value,
                    "date": metric.date.isoformat()
                })
            
            # Создаем отчет
            report_data = {
                "employee_id": employee.id,
                "employee_name": employee.full_name,
                "department": employee.department,
                "position": employee.position,
                "metrics": metrics_data,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # Сохраняем отчет
            crud.report.create(
                db,
                obj_in={
                    "employee_id": employee.id,
                    "report_type": "daily",
                    "start_date": start_date,
                    "end_date": end_date,
                    "data": report_data
                }
            )
            
        return {"status": "success", "message": "Отчеты сгенерированы"}
    finally:
        db.close()

@celery_app.task
def generate_weekly_report():
    """
    Генерация еженедельного отчета
    """
    db = SessionLocal()
    try:
        # Получаем всех сотрудников
        employees = crud.employee.get_employees(db)
        
        for employee in employees:
            # Получаем метрики за последнюю неделю
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(weeks=1)
            
            metrics = crud.metric.get_employee_metrics(
                db, 
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Анализируем метрики
            metrics_data = []
            for metric in metrics:
                metrics_data.append({
                    "type": metric.metric_type,
                    "value": metric.value,
                    "date": metric.date.isoformat()
                })
            
            # Создаем отчет
            report_data = {
                "employee_id": employee.id,
                "employee_name": employee.full_name,
                "department": employee.department,
                "position": employee.position,
                "metrics": metrics_data,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # Сохраняем отчет
            crud.report.create(
                db,
                obj_in={
                    "employee_id": employee.id,
                    "report_type": "weekly",
                    "start_date": start_date,
                    "end_date": end_date,
                    "data": report_data
                }
            )
            
        return {"status": "success", "message": "Отчеты сгенерированы"}
    finally:
        db.close() 