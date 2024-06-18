"""materials

Revision ID: 1f1b03a44b1d
Revises: c372378843aa
Create Date: 2024-05-07 11:24:04.649838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f1b03a44b1d'
down_revision: Union[str, None] = 'c372378843aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column(
        "link_to_material_papers", sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    op.drop_column('experiment', 'link_to_material_papers')
