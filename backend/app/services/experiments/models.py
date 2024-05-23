from sqlmodel import SQLModel, Field, ARRAY, UniqueConstraint, Column, Integer, String, JSON
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict


class ExperimentBase(SQLModel):
    building_id: int | None = Field(default=None)

    # files
    scheme: Dict | None = Field(sa_column=Column(JSON), default=None)
    model_files: Dict | None = Field(sa_column=Column(JSON), default=None)
    test_files: Dict | None = Field(sa_column=Column(JSON), default=None)
    plan_files: Dict | None = Field(sa_column=Column(JSON), default=None)

    # details
    description: str | None = Field(default=None)
    experiment_id: str | None = Field(default=None)
    test_scale: float | None = Field(default=None)
    simultaneous_excitations_nb: int | None = Field(default=None)
    applied_excitation_directions: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    storeys_nb: int | None = Field(default=None)
    building_height: int | None = Field(default=None)
    total_building_height: int | None = Field(default=None)
    diaphragm_material: str | None = Field(default=None)
    roof_material_geometry: str | None = Field(default=None)
    masonry_unit_type: str | None = Field(default=None)
    masonry_unit_material: str | None = Field(default=None)
    mortar_type: str | None = Field(default=None)
    masonry_compressive_strength: int | None = Field(default=None)
    masonry_wall_thickness: List[int] | None = Field(
        sa_column=Column(ARRAY(Integer)), default=None)
    wall_leaves_nb: int | None = Field(default=None)
    internal_walls: bool | None = Field(default=None)
    mechanical_connectors: str | None = Field(default=None)
    connectors_activation: str | None = Field(default=None)
    retrofitted: bool | None = Field(default=None)
    retrofitting_application: str | None = Field(default=None)
    retrofitting_type: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    first_estimated_fundamental_period: float | None = Field(default=None)
    last_estimated_fundamental_period: float | None = Field(default=None)
    max_horizontal_pga: float | None = Field(default=None)
    max_estimated_dg: float | None = Field(default=None)
    material_characterizations: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    associated_test_types: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    material_characterization_refs: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    digitalized_data: bool = Field(default=False)
    experimental_results_reported: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    open_measured_data: bool = Field(default=False)
    link_to_open_measured_data: str | None = Field(default=None)
    crack_types_observed: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)
    experimental_campaign_motivation: str | None = Field(default=None)
    publication_year: int | None = Field(default=None)
    link_to_material_papers: List[str] | None = Field(
        sa_column=Column(ARRAY(String)), default=None)

    reference_id: int = Field(
        foreign_key="reference.id", index=True
    )

    model_config = ConfigDict(
        protected_namespaces=()
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
    masonry_unit_type: str | None
    diaphragm_material: str | None
    wall_leaves_nb: int | None
    storeys_nb: int | None
    test_scale: float | None
    simultaneous_excitations_nb: int | None
    retrofitting_application: str | None
    count: int
