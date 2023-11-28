from pydantic import BaseModel

class RunResultBase(BaseModel):
    run_id: str
    nominal_pga_x: float | None = None
    nominal_pga_y: float | None = None
    nominal_pga_z: float | None = None
    actual_pga_x: float | None = None
    actual_pga_y: float | None = None
    actual_pga_z: float | None = None
    dg_reported: float | None = None
    dg_derived: float | None = None
    max_top_drift_x: float | None = None
    max_top_drift_y: float | None = None
    residual_top_drift_x: float | None = None
    residual_top_drift_y: float | None = None
    base_shear_coef: float | None = None
    reported_t1_x: float | None = None
    reported_t1_y: float | None = None

class RunResultCreate(RunResultBase):
    pass

class RunResult(RunResultBase):
    id: int
    experiment_id: int

    class Config:
        orm_mode = True

class ExperimentBase(BaseModel):
    experiment_id: str | None = None
    test_scale: float | None = None
    simultaneous_excitations_nb: int | None = None
    applied_excitation_directions: list[str] | None = None
    run_results_nb: int | None = None
    storeys_nb: int | None = None
    building_height: int | None = None
    total_building_height: int | None = None
    diaphragm_material: str | None = None
    roof_material_geometry: str | None = None
    masonry_unit_type: str | None = None
    masonry_unit_material: str | None = None
    mortar_type: str | None = None
    masonry_compressive_strength: int | None = None
    masonry_wall_thickness: list[int] | None = None
    wall_leaves_nb: int | None = None
    internal_walls: bool = False
    mechanical_connectors: str | None = None
    connectors_activation: str | None
    retrofitted: bool = False
    retrofitting_application: str | None = None
    retrofitting_type: list[str] | None = None
    first_estimated_fundamental_period: float | None = None
    last_estimated_fundamental_period: float | None = None
    max_horizontal_pga: float | None = None
    max_estimated_dg: float | None = None
    material_characterizations: list[str] | None = None
    associated_test_types: list[str]  | None = None
    material_characterization_refs: list[str] | None = None
    experimental_results_reported: list[str] | None = None
    open_measured_data: bool = False
    link_to_open_measured_data: str | None = None
    digitalized_data: bool = False
    crack_types_observed: list[str] | None = None
    experimental_campaign_motivation: str | None = None

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int
    reference_id: int

    class Config:
        orm_mode = True
