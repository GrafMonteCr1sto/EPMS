from app.worker import celery_app
from app import crud
from app.db.session import SessionLocal
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

@celery_app.task
def update_metrics():
    """
    Обновление метрик эффективности сотрудников
    """
    db = SessionLocal()
    try:
        # Получаем всех сотрудников
        employees = crud.employee.get_employees(db)
        
        # Получаем метрики за последние 30 дней
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        # Собираем метрики для анализа
        metrics_data = []
        for employee in employees:
            metrics = crud.metric.get_employee_metrics(
                db, 
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date
            )
            
            if metrics:
                # Вычисляем средние значения метрик
                avg_metrics = {}
                for metric in metrics:
                    if metric.metric_type not in avg_metrics:
                        avg_metrics[metric.metric_type] = []
                    avg_metrics[metric.metric_type].append(metric.value)
                
                # Добавляем данные для кластеризации
                metrics_data.append({
                    "employee_id": employee.id,
                    "metrics": {k: np.mean(v) for k, v in avg_metrics.items()}
                })
        
        if metrics_data:
            # Подготовка данных для кластеризации
            df = pd.DataFrame(metrics_data)
            X = df["metrics"].apply(pd.Series)
            
            # Нормализация данных
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Кластеризация
            n_clusters = min(5, len(metrics_data))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Обновляем метрики эффективности
            for i, data in enumerate(metrics_data):
                employee_id = data["employee_id"]
                cluster = clusters[i]
                
                # Создаем новую метрику эффективности
                crud.metric.create(
                    db,
                    obj_in={
                        "employee_id": employee_id,
                        "metric_type": "efficiency",
                        "value": float(cluster + 1) / n_clusters,  # Нормализуем значение
                        "date": datetime.utcnow(),
                        "description": f"Кластер эффективности: {cluster + 1}"
                    }
                )
        
        return {"status": "success", "message": "Метрики обновлены"}
    finally:
        db.close()

@celery_app.task
def analyze_trends():
    """
    Анализ трендов эффективности
    """
    db = SessionLocal()
    try:
        # Получаем метрики за последние 90 дней
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        
        # Получаем всех сотрудников
        employees = crud.employee.get_employees(db)
        
        for employee in employees:
            metrics = crud.metric.get_employee_metrics(
                db, 
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date
            )
            
            if metrics:
                # Анализируем тренды
                metrics_by_type = {}
                for metric in metrics:
                    if metric.metric_type not in metrics_by_type:
                        metrics_by_type[metric.metric_type] = []
                    metrics_by_type[metric.metric_type].append({
                        "value": metric.value,
                        "date": metric.date
                    })
                
                # Вычисляем тренды
                trends = {}
                for metric_type, values in metrics_by_type.items():
                    if len(values) > 1:
                        # Сортируем по дате
                        values.sort(key=lambda x: x["date"])
                        # Вычисляем тренд
                        trend = np.polyfit(
                            range(len(values)),
                            [v["value"] for v in values],
                            1
                        )[0]
                        trends[metric_type] = trend
                
                # Создаем отчет о трендах
                if trends:
                    crud.report.create(
                        db,
                        obj_in={
                            "employee_id": employee.id,
                            "report_type": "trends",
                            "start_date": start_date,
                            "end_date": end_date,
                            "data": {
                                "trends": trends,
                                "generated_at": datetime.utcnow().isoformat()
                            }
                        }
                    )
        
        return {"status": "success", "message": "Тренды проанализированы"}
    finally:
        db.close() 