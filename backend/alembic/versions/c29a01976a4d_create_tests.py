"""create_experiments

Revision ID: c29a01976a4d
Revises: 
Create Date: 2023-11-27 11:11:11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c29a01976a4d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reference",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reference", sa.String(), unique=True, index=True),
        sa.Column("publication_year", sa.Integer(), nullable=True),
        sa.Column("link_to_request_data", sa.String(), nullable=True),
        sa.Column("link_to_experimental_paper", sa.String(), nullable=True),
        sa.Column("corresponding_author_name", sa.String(), nullable=True),
        sa.Column("corresponding_author_email", sa.String(), nullable=True),

        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reference_ref"), "reference", ["reference"], unique=False),
    op.create_index(op.f("ix_reference_name"), "reference", ["corresponding_author_name"], unique=False),
    op.create_index(op.f("ix_reference_email"), "reference", ["corresponding_author_email"], unique=False),
    op.create_table(
        "experiment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("experiment_id", sa.String, index=True),
        sa.Column("test_scale", sa.String(), nullable=True),
        sa.Column("simultaneous_excitations_nb", sa.Integer(), nullable=True),
        sa.Column("applied_excitations_direction", sa.String(), nullable=True),
        sa.Column("run_results_nb", sa.Integer(), nullable=True),
        sa.Column("storeys_nb", sa.Integer(), nullable=True),
        sa.Column("total_building_height", sa.Integer(), nullable=True),
        sa.Column("diaphragm_material", sa.String(), nullable=True),
        sa.Column("roof_material_geometry", sa.String(), nullable=True),
        sa.Column("masonry_unit_type", sa.String(), nullable=True),
        sa.Column("masonry_unit_material", sa.String(), nullable=True),
        sa.Column("mortar_type", sa.String(), nullable=True),
        sa.Column("masonry_compressive_strength", sa.Integer(), nullable=True),
        sa.Column("masonry_wall_thickness", sa.Integer(), nullable=True),
        sa.Column("wall_leaves_nb", sa.Integer(), nullable=True),
        sa.Column("internal_walls", sa.String(), nullable=True), # sa.Boolean, default=False),
        sa.Column("mechanical_connectors", sa.String(), nullable=True),
        sa.Column("connectors_activation", sa.String(), nullable=True),
        sa.Column("retrofitted", sa.String(), nullable=True),
        sa.Column("retrofitting_application", sa.String(), nullable=True),
        sa.Column("retrofitting_type", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("first_estimated_fundamental_period", sa.Float(), nullable=True),
        sa.Column("last_estimated_fundamental_period", sa.Float(), nullable=True),
        sa.Column("max_horizontal_pga", sa.Float(), nullable=True),
        sa.Column("max_estimated_dg", sa.Float(), nullable=True),
        sa.Column("material_characterizations", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("associated_test_types", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("material_characterization_refs", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("digitalized_data", sa.String(), nullable=True), # sa.Boolean(), default=False),
        sa.Column("experimental_results_reported", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("open_measured_data", sa.String(), nullable=True),
        sa.Column("crack_types_observed", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("experimental_campaign_motivation", sa.String(), nullable=True),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        
        sa.ForeignKeyConstraint(["reference_id"], ["reference.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiment_description"), "experiment", ["description"], unique=False)
    op.create_index(op.f("ix_experiment_id"), "experiment", ["id"], unique=False)
    op.create_table(
        "run_result",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("nominal_pga_x", sa.Float(), nullable=True),
        sa.Column("nominal_pga_y", sa.Float(), nullable=True),
        sa.Column("nominal_pga_z", sa.Float(), nullable=True),
        sa.Column("actual_pga_x", sa.Float(), nullable=True),
        sa.Column("actual_pga_y", sa.Float(), nullable=True),
        sa.Column("actual_pga_z", sa.Float(), nullable=True),
        sa.Column("reported_dg", sa.Float(), nullable=True),
        sa.Column("derived_dg", sa.Float(), nullable=True),
        sa.Column("max_top_drift", sa.Float(), nullable=True),
        sa.Column("residual_top_drift", sa.Float(), nullable=True),
        sa.Column("base_shear_coef", sa.Float(), nullable=True),
        sa.Column("reported_t1_x", sa.Float(), nullable=True),
        sa.Column("reported_t1_y", sa.Float(), nullable=True),
        sa.Column("experiment_id", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(["experiment_id"], ["experiment.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_run_result_id"), "run_result", ["id"], unique=False)
    op.create_index(op.f("ix_run_result_name"), "run_result", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_run_result_name"), table_name="run_result")
    op.drop_index(op.f("ix_run_result_id"), table_name="run_result")
    op.drop_table("run_result")
    op.drop_index(op.f("ix_experiment_id"), table_name="experiment")
    op.drop_index(op.f("ix_experiment_description"), table_name="experiment")
    op.drop_table("experiment")
    op.drop_index(op.f("ix_reference_email"), table_name="experiment")
    op.drop_index(op.f("ix_reference_name"), table_name="experiment")
    op.drop_index(op.f("ix_reference_ref"), table_name="experiment")
    op.drop_table("reference")
    # ### end Alembic commands ###