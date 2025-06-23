from datetime import datetime
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
from app.crud.charity_project import (
    create_charity_project,
    delete_charity_project,
    get_charity_projects,
    update_charity_project,
)
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
):
    return await get_charity_projects(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    await invest_money(new_project, session)
    return new_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_before_delete(charity_project)
    charity_project = await delete_charity_project(charity_project, session)
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
):
    charity_project = await check_charity_project_exists(project_id, session)
    check_project_before_update(charity_project, obj_in)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await update_charity_project(
        charity_project, obj_in, session
    )

    # Проверяем, нужно ли закрыть проект после обновления
    if charity_project.invested_amount == charity_project.full_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.utcnow()
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project
