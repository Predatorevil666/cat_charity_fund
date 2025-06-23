from fastapi_users.exceptions import UserAlreadyExists

from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


async def create_user(email: str, password: str, is_superuser: bool = False):
    """
    Создает пользователя с указанными email и паролем.
    По умолчанию создается обычный пользователь, но можно создать и суперпользователя.
    """
    try:
        # Получаем объекты асинхронной сессии
        async for session in get_async_session():
            # Получаем объект репозитория для работы с пользователями
            async for user_db in get_user_db(session):
                # Получаем объект менеджера пользователей
                async for user_manager in get_user_manager(user_db):
                    # Создаем объект схемы создания пользователя
                    user_create = UserCreate(
                        email=email,
                        password=password,
                        is_superuser=is_superuser,
                    )
                    try:
                        # Создаем пользователя в базе данных
                        user = await user_manager.create(user_create)
                        print(f"Пользователь {email} успешно создан")
                        return user
                    except UserAlreadyExists:
                        print(f"Пользователь {email} уже существует")
                    except Exception as e:
                        print(f"Ошибка при создании пользователя: {e}")
    except Exception as e:
        print(f"Произошла ошибка при создании пользователя: {e}")
        raise e
