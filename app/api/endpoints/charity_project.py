from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_money

router = APIRouter()


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProject]:
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )

    # Получаем неинвестированные пожертвования
    donations = await donation_crud.get_not_fully_invested(session)

    # Инвестируем деньги и получаем список измененных пожертвований
    modified_donations = invest_money(new_project, donations)

    # Добавляем все измененные объекты в сессию
    for donation in modified_donations:
        session.add(donation)

    # Добавляем проект в сессию и коммитим изменения
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_before_delete(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_before_update(charity_project, obj_in)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    # Проверяем, нужно ли закрыть проект после обновления
    if charity_project.invested_amount == charity_project.full_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now(timezone.utc)
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project
