from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_FULLY_INVESTED, DEFAULT_INVESTED_AMOUNT
from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationDB


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationDB]):
    async def create_donation(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user_id: int,
        commit: bool = True,
    ) -> Donation:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        default_values = {
            "invested_amount": DEFAULT_INVESTED_AMOUNT,
            "fully_invested": DEFAULT_FULLY_INVESTED,
        }
        for field, value in default_values.items():
            if hasattr(db_obj, field) and getattr(db_obj, field) is None:
                setattr(db_obj, field, value)

        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_user_donations(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
