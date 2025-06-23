import asyncio
import os
import subprocess
import sys
from pathlib import Path
from fastapi_users.exceptions import UserAlreadyExists

sys.path.append(".")  # noqa: E402

# Импорты из приложения после добавления пути
from app.core.config import settings  # noqa: E402
from app.core.db import get_async_session  # noqa: E402
from app.core.user import get_user_db, get_user_manager  # noqa: E402
from app.schemas.user import UserCreate  # noqa: E402


# Корутина для создания суперпользователя
async def create_superuser():
    # Получаем объекты асинхронной сессии
    async for session in get_async_session():
        # Получаем объект репозитория для работы с пользователями
        async for user_db in get_user_db(session):
            # Получаем объект менеджера пользователей
            async for user_manager in get_user_manager(user_db):
                # Создаем объект схемы создания пользователя
                user_create = UserCreate(
                    email=settings.first_superuser_email,
                    password=settings.first_superuser_password,
                    is_superuser=True,
                )
                try:
                    # Создаем пользователя в базе данных
                    await user_manager.create(user_create)
                    print("Суперпользователь успешно создан")
                except UserAlreadyExists:
                    print("Суперпользователь уже существует")
                except Exception as e:
                    print(f"Ошибка при создании суперпользователя: {e}")
                return


# Функция для применения миграций
def apply_migrations():
    try:
        # Проверяем, существует ли файл базы данных
        db_file = Path("./fastapi.db")
        if not db_file.exists():
            print("Применение миграций...")
            # Запускаем команду alembic upgrade head
            subprocess.run(["alembic", "upgrade", "head"], check=True)
            print("Миграции успешно применены")
        else:
            print("База данных уже существует, пропускаем миграции")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при применении миграций: {e}")
        sys.exit(1)


# Функция для запуска приложения
def run_app():
    try:
        # Запускаем uvicorn
        os.execvp(
            "uvicorn",
            [
                "uvicorn",
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8003",
            ],
        )
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Применяем миграции
    apply_migrations()

    # Создаем суперпользователя
    asyncio.run(create_superuser())

    # Запускаем приложение
    run_app()
