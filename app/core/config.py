from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки приложения
    APP_NAME: str = "Система мониторинга эффективности сотрудников"
    DEBUG: bool
    SECRET_KEY: str = "your-secret-key-here"
    API_V1_PREFIX: str = "/api/v1"

    # Настройки базы данных PostgreSQL
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str

    # Настройки Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # Настройки JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Настройки логирования
    LOG_LEVEL: str
    LOG_FORMAT: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 