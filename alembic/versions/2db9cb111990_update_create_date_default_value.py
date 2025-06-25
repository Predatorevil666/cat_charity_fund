"""update_create_date_default_value

Revision ID: 2db9cb111990
Revises: new_constraints
Create Date: 2025-06-25 09:50:02.909437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2db9cb111990'
down_revision = 'new_constraints'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite doesn't support ALTER TABLE for changing column constraints
    # This migration is only needed for schema documentation purposes
    # The actual changes are already in the model definitions
    pass


def downgrade():
    # SQLite doesn't support ALTER TABLE for changing column constraints
    # No changes needed for downgrade
    pass 