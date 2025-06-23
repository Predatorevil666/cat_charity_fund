from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.schemas.donation import DonationCreate


async def create_donation(
    new_donation: DonationCreate,
    session: AsyncSession,
    user_id: int,
) -> Donation:
    new_donation_data = new_donation.model_dump()
    db_donation = Donation(**new_donation_data, user_id=user_id)
    session.add(db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


async def get_donation(
    donation_id: int,
    session: AsyncSession,
) -> Optional[Donation]:
    db_donation = await session.execute(
        select(Donation).where(Donation.id == donation_id)
    )
    return db_donation.scalars().first()


async def get_donations(
    session: AsyncSession,
) -> List[Donation]:
    donations = await session.execute(select(Donation))
    return donations.scalars().all()


async def get_user_donations(
    session: AsyncSession,
    user_id: int,
) -> List[Donation]:
    donations = await session.execute(
        select(Donation).where(Donation.user_id == user_id)
    )
    return donations.scalars().all()
