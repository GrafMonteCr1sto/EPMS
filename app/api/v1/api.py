from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    employees,
    metrics,
    analytics,
    recommendations,
    reports
)

api_router = APIRouter()

# Подключение эндпоинтов
api_router.include_router(auth.router, prefix="/auth", tags=["Аутентификация"])
api_router.include_router(employees.router, prefix="/employees", tags=["Сотрудники"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Метрики"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Аналитика"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Рекомендации"])
api_router.include_router(reports.router, prefix="/reports", tags=["Отчеты"]) 