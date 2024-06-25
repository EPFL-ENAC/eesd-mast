"""models_view

Revision ID: 125fb95f2eca
Revises: 141caa602606
Create Date: 2024-06-25 10:12:17.633840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '125fb95f2eca'
down_revision: Union[str, None] = '141caa602606'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the view
    op.execute("""
    CREATE VIEW expcount AS
    SELECT 
      id,
      masonry_unit_material,
      masonry_unit_type,
      diaphragm_material,
      wall_leaves_nb,
      storeys_nb,
      test_scale,
      simultaneous_excitations_nb,
      retrofitting_application,
      (CASE WHEN (CAST(model_files AS VARCHAR) != 'null' AND model_files IS NOT NULL) THEN 1 ELSE 0 END) AS model_files
    FROM experiment
    """)


def downgrade() -> None:
    # Drop the view
    op.execute("DROP VIEW expcount")
