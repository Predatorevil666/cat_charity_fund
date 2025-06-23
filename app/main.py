from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_users.exceptions import InvalidPasswordException

from app.api.exception_handlers import (
    validation_exception_handler,
    invalid_password_exception_handler
)
from app.api.routers import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(router)

# Регистрируем обработчики исключений
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)
app.add_exception_handler(
    InvalidPasswordException,
    invalid_password_exception_handler
)
