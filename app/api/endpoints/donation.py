from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import (
    create_donation,
    get_donations,
    get_user_donations,
)
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBFull
from app.services.investment import invest_money

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await create_donation(donation, session, user.id)
    await invest_money(new_donation, session)
    return new_donation


@router.get(
    "/",
    response_model=List[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_donations(session)


@router.get(
    "/my",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await get_user_donations(session, user.id)
