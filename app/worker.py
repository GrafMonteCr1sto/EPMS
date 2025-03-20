from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "epms",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
)

# Настройка периодических задач
celery_app.conf.beat_schedule = {
    "generate-daily-reports": {
        "task": "app.tasks.reports.generate_daily_report",
        "schedule": 86400.0,  # каждые 24 часа
    },
    "generate-weekly-reports": {
        "task": "app.tasks.reports.generate_weekly_report",
        "schedule": 604800.0,  # каждые 7 дней
    },
    "update-metrics": {
        "task": "app.tasks.metrics.update_metrics",
        "schedule": 3600.0,  # каждый час
    },
    "analyze-trends": {
        "task": "app.tasks.metrics.analyze_trends",
        "schedule": 86400.0,  # каждые 24 часа
    },
} 