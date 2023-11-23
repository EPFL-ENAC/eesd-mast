from pydantic import BaseModel

class TestRunBase(BaseModel):
    name: str
    nominal_pga_x: float | None = None
    nominal_pga_y: float | None = None
    nominal_pga_z: float | None = None
    actual_pga_x: float | None = None
    actual_pga_y: float | None = None
    actual_pga_z: float | None = None
    reported_dg: float | None = None
    derived_dg: float | None = None
    max_top_drift: float | None = None
    residual_top_drift: float | None = None
    base_shear_coef: float | None = None
    reported_t1_x: float | None = None
    reported_t1_y: float | None = None

class TestRunCreate(TestRunBase):
    pass

class TestRun(TestRunBase):
    id: int
    test_summary_id: int

    class Config:
        orm_mode = True

class TestSummaryBase(BaseModel):
    experiment_id: str
    test_scale: str | None = None
    simultaneous_excitations_nb: int | None = None
    applied_excitations_direction: str | None = None
    test_runs_nb: int | None = None
    storeys_nb: int | None = None
    total_building_height: int | None = None
    diaphragm_material: str | None = None
    roof_material_geometry: str | None = None
    masonry_unit_type: str | None = None
    masonry_unit_material: str | None = None
    mortar_type: str | None = None
    masonry_compressive_strength: int | None = None
    masonry_wall_thickness: int | None = None
    wall_leaves_nb: int | None = None
    internal_walls: str | None # bool = False
    mechanical_connectors: str | None = None
    connectors_activation: str | None # bool = False
    retrofitted: str | None # bool = False
    retrofitting_application: str | None = None
    retrofitting_type: list[str] = []
    first_estimated_fundamental_period: float | None = None
    last_estimated_fundamental_period: float | None = None
    max_horizontal_pga: float | None = None
    max_estimated_dg: float | None = None
    material_characterizations: list[str] = []
    associated_test_types: list[str] = []
    material_characterization_ref: str | None = None
    experimental_results_reported: list[str] = []
    open_measured_data: str | None = None
    link_to_request_data: str | None = None
    digitalized_data: str | None # bool = False
    crack_types_observed: list[str] = []
    experimental_campaign_motivation: str | None = None
    link_to_experimental_paper: str | None = None
    corresponding_author_name: str | None = None
    corresponding_author_email: str | None = None

class TestSummaryCreate(TestSummaryBase):
    pass

class TestSummary(TestSummaryBase):
    id: int

    test_runs: list[TestRun] = []

    class Config:
        orm_mode = True
