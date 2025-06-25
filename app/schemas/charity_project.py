from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import (
    MAX_PROJECT_NAME_LENGTH,
    MIN_AMOUNT,
    MIN_STRING_LENGTH,
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=MAX_PROJECT_NAME_LENGTH)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None, gt=MIN_AMOUNT)

    model_config = ConfigDict(str_min_length=MIN_STRING_LENGTH, extra="forbid")


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=MAX_PROJECT_NAME_LENGTH)
    description: str = Field(...)
    full_amount: int = Field(..., gt=MIN_AMOUNT)


class CharityProjectUpdate(CharityProjectBase):
    @field_validator("name")
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("Имя проекта не может быть пустым!")
        return value

    @field_validator("description")
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("Описание проекта не может быть пустым!")
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
