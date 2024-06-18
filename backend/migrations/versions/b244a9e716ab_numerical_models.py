"""numerical_models

Revision ID: b244a9e716ab
Revises: 1f1b03a44b1d
Create Date: 2024-05-16 08:22:56.130144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b244a9e716ab'
down_revision: Union[str, None] = '1f1b03a44b1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "numericalmodel",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("software_used", sa.String(), nullable=True),
        sa.Column("software_used_comment", sa.String(), nullable=True),
        sa.Column("modeling_approach", sa.String(), nullable=True),
        sa.Column("modeling_approach_comment", sa.String(), nullable=True),
        sa.Column("units", sa.String(), nullable=True),
        sa.Column("units_comment", sa.String(), nullable=True),
        sa.Column("frame_elements", sa.String(), nullable=True),
        sa.Column("frame_elements_comment", sa.String(), nullable=True),
        sa.Column("diaphragm_elements", sa.String(), nullable=True),
        sa.Column("diaphragm_elements_comment", sa.String(), nullable=True),
        sa.Column("damping_model", sa.String(), nullable=True),
        sa.Column("damping_model_comment", sa.String(), nullable=True),
        sa.Column("global_geometry_def", sa.String(), nullable=True),
        sa.Column("global_geometry_def_comment", sa.String(), nullable=True),
        sa.Column("element_geometry_def", sa.String(), nullable=True),
        sa.Column("element_geometry_def_comment", sa.String(), nullable=True),
        sa.Column("mass_def", sa.String(), nullable=True),
        sa.Column("mass_def_comment", sa.String(), nullable=True),
        sa.Column("gravity_loads_def", sa.String(), nullable=True),
        sa.Column("gravity_loads_def_comment", sa.String(), nullable=True),
        sa.Column("wall_connections", sa.String(), nullable=True),
        sa.Column("wall_connections_comment", sa.String(), nullable=True),
        sa.Column("floor_connections", sa.String(), nullable=True),
        sa.Column("floor_connections_comment", sa.String(), nullable=True),
        sa.Column("base_support", sa.String(), nullable=True),
        sa.Column("base_support_comment", sa.String(), nullable=True),

        sa.Column("elastic_modulus", sa.Integer(), nullable=True),
        sa.Column("elastic_modulus_comment", sa.String(), nullable=True),
        sa.Column("shear_modulus", sa.Float(), nullable=True),
        sa.Column("shear_modulus_comment", sa.String(), nullable=True),
        sa.Column("compression_strength", sa.Float(), nullable=True),
        sa.Column("compression_strength_comment", sa.String(), nullable=True),
        sa.Column("tension_strength", sa.Float(), nullable=True),
        sa.Column("tension_strength_comment", sa.String(), nullable=True),
        sa.Column("cohesion", sa.Float(), nullable=True),
        sa.Column("cohesion_comment", sa.String(), nullable=True),
        sa.Column("friction_coeff", sa.Float(), nullable=True),
        sa.Column("friction_coeff_comment", sa.String(), nullable=True),
        sa.Column("residual_friction_coeff", sa.Float(), nullable=True),
        sa.Column("residual_friction_coeff_comment",
                  sa.String(), nullable=True),
        sa.Column("damping_ratio", sa.Float(), nullable=True),
        sa.Column("damping_ratio_comment", sa.String(), nullable=True),
        sa.Column("softening_coeff", sa.Float(), nullable=True),
        sa.Column("softening_coeff_comment", sa.String(), nullable=True),

        sa.Column("experiment_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_numericalmodel_id"),
                    "numericalmodel", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_numericalmodel_id"), table_name="numericalmodel")
    op.drop_table("numericalmodel")
