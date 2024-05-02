"""building-id

Revision ID: 51e5feabdf3a
Revises: e966323d5395
Create Date: 2024-05-02 10:31:06.750991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '51e5feabdf3a'
down_revision: Union[str, None] = 'e966323d5395'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column(
        "building_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('experiment', 'building_id')
