"""building-plans

Revision ID: c372378843aa
Revises: 51e5feabdf3a
Create Date: 2024-05-07 09:55:50.765766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c372378843aa'
down_revision: Union[str, None] = '51e5feabdf3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('experiment', sa.Column(
        "plan_files", sa.JSON(), nullable=True))
    op.alter_column('experiment', 'files', new_column_name='test_files')
    op.alter_column('experiment', 'models', new_column_name='model_files')


def downgrade() -> None:
    op.drop_column('experiment', 'plan_files')
    op.alter_column('experiment', 'test_files', new_column_name='files')
    op.alter_column('experiment', 'model_files', new_column_name='models')
