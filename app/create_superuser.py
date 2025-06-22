import asyncio
import sys

from fastapi_users.exceptions import UserAlreadyExists

sys.path.append(".")

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


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


if __name__ == "__main__":
    asyncio.run(create_superuser())
