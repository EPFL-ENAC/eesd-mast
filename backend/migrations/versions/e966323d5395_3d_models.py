"""3d-models

Revision ID: e966323d5395
Revises: 8e85e114bded
Create Date: 2024-05-01 14:58:11.386721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e966323d5395'
down_revision: Union[str, None] = '8e85e114bded'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column("models", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('experiment', 'models')
