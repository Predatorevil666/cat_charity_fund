from sqlalchemy import Column, String, Text

from app.core.constants import MAX_PROJECT_NAME_LENGTH
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(MAX_PROJECT_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
