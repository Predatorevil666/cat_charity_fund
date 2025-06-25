"""new constraints

Revision ID: new_constraints
Revises: initial_migration
Create Date: 2023-06-12 12:00:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'new_constraints'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite не поддерживает ALTER TABLE для добавления ограничений CHECK
    # Эта миграция только для документирования изменений
    # Ограничения будут применены при создании новых таблиц
    pass


def downgrade():
    pass 