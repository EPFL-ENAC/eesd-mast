from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Dict, Optional


class NumericalModelBase(SQLModel):
    # general information
    software_used: str | None = Field(default=None)
    software_used_comment: str | None = Field(default=None)
    modeling_approach: str | None = Field(default=None)
    modeling_approach_comment: str | None = Field(default=None)
    units: str | None = Field(default=None)
    units_comment: str | None = Field(default=None)
    frame_elements: str | None = Field(default=None)
    frame_elements_comment: str | None = Field(default=None)
    diaphragm_elements: str | None = Field(default=None)
    diaphragm_elements_comment: str | None = Field(default=None)
    damping_model: str | None = Field(default=None)
    damping_model_comment: str | None = Field(default=None)
    global_geometry_def: str | None = Field(default=None)
    global_geometry_def_comment: str | None = Field(default=None)
    element_geometry_def: str | None = Field(default=None)
    element_geometry_def_comment: str | None = Field(default=None)
    mass_def: str | None = Field(default=None)
    mass_def_comment: str | None = Field(default=None)
    gravity_loads_def: str | None = Field(default=None)
    gravity_loads_def_comment: str | None = Field(default=None)
    wall_connections: str | None = Field(default=None)
    wall_connections_comment: str | None = Field(default=None)
    floor_connections: str | None = Field(default=None)
    floor_connections_comment: str | None = Field(default=None)
    base_support: str | None = Field(default=None)
    base_support_comment: str | None = Field(default=None)

    # initial material properties
    elastic_modulus: int | None = Field(default=None)
    elastic_modulus_comment: str | None = Field(default=None)
    shear_modulus: float | None = Field(default=None)
    shear_modulus_comment: str | None = Field(default=None)
    compression_strength: float | None = Field(default=None)
    compression_strength_comment: str | None = Field(default=None)
    tension_strength: float | None = Field(default=None)
    tension_strength_comment: str | None = Field(default=None)
    cohesion: float | None = Field(default=None)
    cohesion_comment: str | None = Field(default=None)
    friction_coeff: float | None = Field(default=None)
    friction_coeff_comment: str | None = Field(default=None)
    residual_friction_coeff: float | None = Field(default=None)
    residual_friction_coeff_comment: str | None = Field(default=None)
    damping_ratio: float | None = Field(default=None)
    damping_ratio_comment: str | None = Field(default=None)
    softening_coeff: float | None = Field(default=None)
    softening_coeff_comment: str | None = Field(default=None)

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
