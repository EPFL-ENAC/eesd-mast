"""experiment_year

Revision ID: 8e85e114bded
Revises: 16aea2c3ecca
Create Date: 2024-03-06 13:00:32.207011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8e85e114bded'
down_revision: Union[str, None] = '16aea2c3ecca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column(
        "publication_year", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('experiment', 'publication_year')
