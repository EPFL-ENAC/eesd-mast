from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Dict, Optional


class NumericalModelBase(SQLModel):
    # general information
    software_used: str | None
    software_used_comment: str | None
    modeling_approach: str | None
    modeling_approach_comment: str | None
    units: str | None
    units_comment: str | None
    frame_elements: str | None
    frame_elements_comment: str | None
    diaphragm_elements: str | None
    diaphragm_elements_comment: str | None
    damping_model: str | None
    damping_model_comment: str | None
    global_geometry_def: str | None
    global_geometry_def_comment: str | None
    element_geometry_def: str | None
    element_geometry_def_comment: str | None
    mass_def: str | None
    mass_def_comment: str | None
    gravity_loads_def: str | None
    gravity_loads_def_comment: str | None
    wall_connections: str | None
    wall_connections_comment: str | None
    floor_connections: str | None
    floor_connections_comment: str | None
    base_support: str | None
    base_support_comment: str | None

    # initial material properties
    elastic_modulus: int | None
    elastic_modulus_comment: str | None
    shear_modulus: float | None
    shear_modulus_comment: str | None
    compression_strength: float | None
    compression_strength_comment: str | None
    tension_strength: float | None
    tension_strength_comment: str | None
    cohesion: float | None
    cohesion_comment: str | None
    friction_coeff: float | None
    friction_coeff_comment: str | None
    residual_friction_coeff: float | None
    residual_friction_coeff_comment: str | None
    damping_ratio: float | None
    damping_ratio_comment: str | None
    softening_coeff: float | None
    softening_coeff_comment: str | None

    experiment_id: int = Field(
        default=None, foreign_key="experiment.id", index=True
    )


class NumericalModel(NumericalModelBase, table=True):
    __table_args__ = (UniqueConstraint("id"),)
    id: int = Field(
        default=None,
        nullable=False,
        primary_key=True,
        index=True,
    )


class NumericalModelRead(NumericalModelBase):
    id: int


class NumericalModelCreate(NumericalModelBase):
    pass


class NumericalModelUpdate(NumericalModelBase):
    pass
