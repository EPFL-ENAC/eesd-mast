"""building_heights

Revision ID: 141caa602606
Revises: b244a9e716ab
Create Date: 2024-06-20 09:20:25.342516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '141caa602606'
down_revision: Union[str, None] = 'b244a9e716ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("experiment", "building_height",
                    existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column("experiment", "total_building_height",
                    existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column("experiment", "masonry_compressive_strength",
                    existing_type=sa.Integer(), type_=sa.Float())


def downgrade() -> None:
    op.alter_column("experiment", "building_height",
                    existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column("experiment", "total_building_height",
                    existing_type=sa.Float(), type_=sa.Integer())
    op.alter_column("experiment", "masonry_compressive_strength",
                    existing_type=sa.Float(), type_=sa.Integer())
