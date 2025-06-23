from fastapi import APIRouter, Depends, HTTPException

from app.core.user import (
    auth_backend,
    current_superuser,
    current_user,
    fastapi_users,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/auth/jwt/logout", tags=["auth"])
async def logout(user: User = Depends(current_user)):
    """
    Эндпоинт для выхода из системы.
    Требует валидный токен аутентификации.
    """
    return {}


# Определяем кастомный эндпоинт для удаления пользователя до
# подключения роутеров fastapi_users
@router.delete("/users/{id}", tags=["users"], deprecated=True)
def delete_user(id: str, user: User = Depends(current_superuser)):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405, detail="Удаление пользователей запрещено!"
    )


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
