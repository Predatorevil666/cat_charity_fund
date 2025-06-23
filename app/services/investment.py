from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_not_fully_invested_objects(
    obj_in: Union[CharityProject, Donation], session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    model = CharityProject if isinstance(obj_in, Donation) else Donation
    objects = await session.execute(
        select(model)
        .where(model.fully_invested.is_(False))
        .order_by(model.create_date)
    )
    return objects.scalars().all()


async def invest_money(
    obj_in: Union[CharityProject, Donation], session: AsyncSession
) -> Union[CharityProject, Donation]:
    objects = await get_not_fully_invested_objects(obj_in, session)

    if not objects:
        return obj_in

    obj_in_need = obj_in.full_amount - obj_in.invested_amount

    for obj in objects:
        obj_available = obj.full_amount - obj.invested_amount

        if obj_in_need >= obj_available:
            obj_in.invested_amount += obj_available
            obj.invested_amount = obj.full_amount
            obj.fully_invested = True
            obj.close_date = datetime.utcnow()
            obj_in_need -= obj_available
        else:
            obj.invested_amount += obj_in_need
            obj_in.invested_amount += obj_in_need

            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()

            if obj_in.invested_amount == obj_in.full_amount:
                obj_in.fully_invested = True
                obj_in.close_date = datetime.utcnow()

            break

        session.add(obj)

        if obj_in_need <= 0:
            break

    # Проверяем, полностью ли инвестирован объект
    if obj_in.invested_amount == obj_in.full_amount:
        obj_in.fully_invested = True
        obj_in.close_date = datetime.utcnow()

    session.add(obj_in)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in
