from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_users.exceptions import InvalidPasswordException

from app.api.routers import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(router)


# Добавляем обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    # Создаем копию ошибок без поля 'input'
    filtered_errors = []

    # Определяем, к какому эндпоинту был запрос
    path = request.url.path

    for error in exc.errors():
        # Копируем ошибку для возможного изменения
        error_copy = dict(error)

        # Удаляем поле 'input' из всех ошибок
        if "input" in error_copy:
            del error_copy["input"]

        # Проверяем, является ли запрос к charity_project или donation
        is_charity_or_donation = path.startswith(
            "/charity_project"
        ) or path.startswith("/donation")

        # Если это не запрос к charity_project или donation, удаляем поле 'ctx'
        if "ctx" in error_copy and not is_charity_or_donation:
            del error_copy["ctx"]

        # Для запросов к charity_project и donation, убедимся, что поле ctx есть в ответе
        # если оно было в исходной ошибке
        if is_charity_or_donation and "ctx" in error:
            error_copy["ctx"] = error["ctx"]

        filtered_errors.append(error_copy)

    # Возвращаем стандартный ответ об ошибке, но с отфильтрованными данными
    return JSONResponse(
        status_code=422,
        content={"detail": filtered_errors},
    )


@app.exception_handler(InvalidPasswordException)
async def invalid_password_exception_handler(
    request: Request, exc: InvalidPasswordException
):
    # Формируем ответ в соответствии с ожидаемой схемой
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": {"code": "invalid_password", "reason": str(exc.reason)}
        },
    )
