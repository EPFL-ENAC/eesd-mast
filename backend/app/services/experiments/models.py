from sqlmodel import SQLModel, Field, ARRAY, UniqueConstraint, Column, Integer, String, JSON
from typing import List, Dict, Optional
from pydantic import BaseModel


class ExperimentBase(SQLModel):
    scheme: Dict | None = Field(sa_column=Column(JSON))
    files: Dict | None = Field(sa_column=Column(JSON))
    description: str | None
    experiment_id: str | None
    test_scale: float | None
    simultaneous_excitations_nb: int | None
    applied_excitation_directions: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    storeys_nb: int | None
    building_height: int | None
    total_building_height: int | None
    diaphragm_material: str | None
    roof_material_geometry: str | None
    masonry_unit_type: str | None
    masonry_unit_material: str | None
    mortar_type: str | None
    masonry_compressive_strength: int | None
    masonry_wall_thickness: List[int] | None = Field(
        sa_column=Column(ARRAY(Integer)))
    wall_leaves_nb: int | None
    internal_walls: bool | None
    mechanical_connectors: str | None
    connectors_activation: str | None
    retrofitted: bool | None
    retrofitting_application: str | None
    retrofitting_type: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    first_estimated_fundamental_period: float | None
    last_estimated_fundamental_period: float | None
    max_horizontal_pga: float | None
    max_estimated_dg: float | None
    material_characterizations: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    associated_test_types: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    material_characterization_refs: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    digitalized_data: bool = Field(default=False)
    experimental_results_reported: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    open_measured_data: bool = Field(default=False)
    link_to_open_measured_data: str | None
    crack_types_observed: List[str] | None = Field(
        sa_column=Column(ARRAY(String)))
    experimental_campaign_motivation: str | None
    publication_year: int | None

    reference_id: int = Field(
        foreign_key="reference.id", index=True
    )


class Experiment(ExperimentBase, table=True):
    __table_args__ = (UniqueConstraint("id"),)
    id: int = Field(
        default=None,
        nullable=False,
        primary_key=True,
        index=True,
    )


class ExperimentRead(ExperimentBase):
    id: int
    reference: Optional[Dict] = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(ExperimentBase):
    pass


class ExperimentFrequencies(BaseModel):
    masonry_unit_material: dict
    diaphragm_material: dict
    storeys_nb: dict
    test_scale: dict


class ExperimentParallelCount(BaseModel):
    masonry_unit_material: str | None
    diaphragm_material: str | None
    storeys_nb: int | None
    test_scale: float | None
    count: int
