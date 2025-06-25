"""use_constant_for_project_name_length

Revision ID: 85952bc4a7d2
Revises: 2db9cb111990
Create Date: 2025-06-25 09:56:47.980331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85952bc4a7d2'
down_revision = '2db9cb111990'
branch_labels = None
depends_on = None


def upgrade():
    # This migration is for documentation purposes only
    # We've moved the hardcoded value 100 for CharityProject.name length
    # to a constant MAX_PROJECT_NAME_LENGTH in app/core/constants.py
    pass


def downgrade():
    # No changes needed for downgrade
    pass 