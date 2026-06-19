from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    # Base de dados
    DATABASE_URL: str = "sqlite:///./carsite.db"

    # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]

    # CORS — domínios do frontend
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    # App
    DEBUG: bool = False
    APP_TITLE: str = "CarSite API"
    APP_VERSION: str = "1.0.0"

    # URL base para as fotos (usa o teu domínio em produção)
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
