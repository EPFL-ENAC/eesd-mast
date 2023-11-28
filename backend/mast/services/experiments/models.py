from sqlalchemy import Boolean, Column, ForeignKey, Float, Integer, String, ARRAY
from sqlalchemy.ext.mutable import MutableList

from mast.database import Base

class Experiment(Base):
    __tablename__ = "experiment"

    id = Column(Integer, primary_key=True, index=True)
    # TODO scheme
    description = Column(String)
    experiment_id = Column(String, unique=True, index=True)
    test_scale = Column(Float)
    simultaneous_excitations_nb = Column(Integer)
    applied_excitation_directions = Column(MutableList.as_mutable(ARRAY(String)))
    run_results_nb = Column(Integer)
    storeys_nb = Column(Integer)
    building_height = Column(Integer)
    total_building_height = Column(Integer)
    diaphragm_material = Column(String)
    roof_material_geometry = Column(String)
    masonry_unit_type = Column(String)
    masonry_unit_material = Column(String)
    mortar_type = Column(String)
    masonry_compressive_strength = Column(Integer)
    masonry_wall_thickness = Column(MutableList.as_mutable(ARRAY(Integer)))
    wall_leaves_nb = Column(Integer)
    internal_walls = Column(String) # Column(Boolean, default=False)
    mechanical_connectors = Column(String)
    connectors_activation = Column(String) # Column(Boolean, default=False)
    retrofitted = Column(String) # Column(Boolean, default=False)
    retrofitting_application = Column(String)
    retrofitting_type = Column(MutableList.as_mutable(ARRAY(String)))
    first_estimated_fundamental_period = Column(Float)
    last_estimated_fundamental_period = Column(Float)
    max_horizontal_pga = Column(Float)
    max_estimated_dg = Column(Float)
    material_characterizations = Column(MutableList.as_mutable(ARRAY(String)))
    associated_test_types = Column(MutableList.as_mutable(ARRAY(String)))
    material_characterization_refs = Column(MutableList.as_mutable(ARRAY(String)))
    digitalized_data = Column(Boolean, default=False)
    experimental_results_reported = Column(MutableList.as_mutable(ARRAY(String)))
    open_measured_data = Column(Boolean, default=False)
    link_to_open_measured_data = Column(String)
    crack_types_observed = Column(MutableList.as_mutable(ARRAY(String)))
    experimental_campaign_motivation = Column(String)

    reference_id = Column(Integer, ForeignKey("reference.id"))

class RunResult(Base):
    __tablename__ = "run_result"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, unique=True, index=True)
    nominal_pga_x = Column(Float)
    nominal_pga_y = Column(Float)
    nominal_pga_z = Column(Float)
    actual_pga_x = Column(Float)
    actual_pga_y = Column(Float)
    actual_pga_z = Column(Float)
    dg_reported = Column(Float)
    dg_derived = Column(Float)
    max_top_drift_x = Column(Float)
    max_top_drift_y = Column(Float)
    residual_top_drift_x = Column(Float)
    residual_top_drift_y = Column(Float)
    base_shear_coef = Column(Float)
    reported_t1_x = Column(Float)
    reported_t1_y = Column(Float)

    experiment_id = Column(Integer, ForeignKey("experiment.id"))
