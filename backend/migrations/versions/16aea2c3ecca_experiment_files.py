"""experiment_files

Revision ID: 16aea2c3ecca
Revises: c29a01976a4d
Create Date: 2024-01-16 15:56:47.168854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '16aea2c3ecca'
down_revision: Union[str, None] = 'c29a01976a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column("files", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('experiment', 'files')
