"""refactor_investment_function

Revision ID: 6799a98ae380
Revises: 85952bc4a7d2
Create Date: 2025-06-25 10:19:11.499210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6799a98ae380'
down_revision = '85952bc4a7d2'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite не поддерживает ALTER TABLE для изменения ограничений колонок
    # Эта миграция только для документирования изменений:
    # 1. Рефакторинг функции инвестирования:
    #    - Перенос get_not_fully_invested_objects в CRUD
    #    - Изменение функции invest_money на не-асинхронную
    #    - Изменение параметров функции invest_money (target, sources)
    #    - Возврат списка измененных объектов
    pass


def downgrade():
    # SQLite не поддерживает ALTER TABLE для изменения ограничений колонок
    # Нет необходимости в откате
    pass 