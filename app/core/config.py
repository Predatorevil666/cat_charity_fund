from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Кошачий благотворительный фонд"
    app_description: str = "Описание проекта по умолчанию"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    
    # Настройки для первого суперпользователя
    first_superuser_email: Optional[EmailStr] = "admin@example.com"
    first_superuser_password: Optional[str] = "admin"

    class Config:
        env_file = ".env"


settings = Settings()
