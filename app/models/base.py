from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.constants import DEFAULT_FULLY_INVESTED, DEFAULT_INVESTED_AMOUNT
from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, default=DEFAULT_INVESTED_AMOUNT, nullable=False
    )
    fully_invested = Column(
        Boolean, default=DEFAULT_FULLY_INVESTED, nullable=False
    )
    create_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "invested_amount >= 0", name="check_invested_amount_positive"
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name="check_invested_amount_not_exceed",
        ),
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount}, "
            f"fully_invested={self.fully_invested}, "
            f"create_date={self.create_date}, "
            f"close_date={self.close_date}"
            f")>"
        )
