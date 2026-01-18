# app/config.py

from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "connectsphere"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://postgres:ahmed1234@localhost:3202/sentiment"

    # Security
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # File Upload
    MAX_FILE_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "mp4", "mov"]

    @validator("ALLOWED_EXTENSIONS", pre=True)
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

    # Email (optional)
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = 587
    MAIL_SERVER: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/avatars", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/posts", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/stories", exist_ok=True)