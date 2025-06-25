from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
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
    new_donation = await donation_crud.create_donation(
        donation, session, user.id, commit=False
    )

    # Получаем неинвестированные проекты
    projects = await charity_project_crud.get_not_fully_invested(session)

    # Инвестируем деньги и получаем список измененных проектов
    modified_projects = invest_money(new_donation, projects)

    # Добавляем все измененные объекты в сессию
    for project in modified_projects:
        session.add(project)

    # Добавляем пожертвование в сессию и коммитим изменения
    session.add(new_donation)
    await session.commit()
    await session.refresh(new_donation)

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
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_user_donations(session, user.id)
