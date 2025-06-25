from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return project


def check_project_before_delete(
    charity_project: CharityProject,
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


def check_project_before_update(
    charity_project: CharityProject,
    obj_in: CharityProjectUpdate,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )
    if obj_in.full_amount and (
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=400,
            detail=("Нельзя установить сумму меньше уже вложенной в проект!"),
        )
