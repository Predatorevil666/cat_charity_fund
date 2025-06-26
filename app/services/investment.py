from datetime import datetime, timezone
from typing import List, TypeVar

from app.core.constants import DEFAULT_INVESTED_AMOUNT
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


def check_and_close_obj(obj: ModelType) -> None:
    """
    Проверяет, полностью ли инвестирован объект, и если да, то закрывает его.

    Args:
        obj: Объект для проверки
    """
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now(timezone.utc)


def invest_money(
    target: ModelType,
    sources: List[ModelType],
) -> List[ModelType]:
    """
    Инвестирование средств.

    Args:
        target: Целевой объект для инвестирования (проект или пожертвование)
        sources: Список объектов для инвестирования в target

    Returns:
        List[ModelType]: Список измененных объектов из sources
    """
    # Убедимся, что invested_amount инициализирован
    if target.invested_amount is None:
        target.invested_amount = DEFAULT_INVESTED_AMOUNT

    # Список измененных объектов
    modified_objects: List[ModelType] = []

    # Сколько средств нужно инвестировать в target
    target_need = target.full_amount - target.invested_amount

    # Если нечего инвестировать, возвращаем пустой список
    if target_need <= 0:
        return modified_objects

    # Обходим все источники средств
    for source in sources:
        # Убедимся, что invested_amount инициализирован в объекте
        if source.invested_amount is None:
            source.invested_amount = DEFAULT_INVESTED_AMOUNT

        # Сколько средств доступно в текущем источнике
        source_available = source.full_amount - source.invested_amount

        # Определяем сумму для инвестирования в этой итерации
        to_invest = min(target_need, source_available)

        # Если нечего инвестировать, прерываем цикл
        if to_invest <= 0:
            break

        # Инвестируем средства
        source.invested_amount += to_invest
        target.invested_amount += to_invest

        # Проверяем и закрываем объекты при необходимости
        check_and_close_obj(source)
        check_and_close_obj(target)

        # Добавляем источник в список измененных объектов
        modified_objects.append(source)

        # Уменьшаем сумму, которую нужно инвестировать
        target_need -= to_invest

        # Если целевой объект полностью инвестирован, прерываем цикл
        if target_need <= 0:
            break

    # Возвращаем список измененных объектов
    return modified_objects
