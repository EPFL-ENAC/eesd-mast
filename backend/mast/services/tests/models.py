from sqlalchemy import Boolean, Column, ForeignKey, Float, Integer, String, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from mast.database import Base

class TestSummary(Base):
    __tablename__ = "test_summary"

    id = Column(Integer, primary_key=True, index=True)
    # TODO scheme
    reference = Column(String)
    publication_year = Column(Integer)
    description = Column(String)
    experiment_id = Column(String, unique=True, index=True)
    test_scale = Column(String)
    simultaneous_excitations_nb = Column(Integer)
    applied_excitations_direction = Column(String)
    test_runs_nb = Column(Integer)
    storeys_nb = Column(Integer)
    total_building_height = Column(Integer)
    diaphragm_material = Column(String)
    roof_material_geometry = Column(String)
    masonry_unit_type = Column(String)
    masonry_unit_material = Column(String)
    mortar_type = Column(String)
    masonry_compressive_strength = Column(Integer)
    masonry_wall_thickness = Column(Integer)
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
    material_characterization_ref = Column(String)
    experimental_results_reported = Column(MutableList.as_mutable(ARRAY(String)))
    open_measured_data = Column(String)
    link_to_request_data = Column(String)
    digitalized_data = Column(String) # Column(Boolean, default=False)
    crack_types_observed = Column(MutableList.as_mutable(ARRAY(String)))
    experimental_campaign_motivation = Column(String)
    link_to_experimental_paper = Column(String)
    corresponding_author_name = Column(String)
    corresponding_author_email = Column(String)

    test_runs = relationship("TestRun", back_populates="test")

class TestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    nominal_pga_x = Column(Float)
    nominal_pga_y = Column(Float)
    nominal_pga_z = Column(Float)
    actual_pga_x = Column(Float)
    actual_pga_y = Column(Float)
    actual_pga_z = Column(Float)
    reported_dg = Column(Float)
    derived_dg = Column(Float)
    max_top_drift = Column(Float)
    residual_top_drift = Column(Float)
    base_shear_coef = Column(Float)
    reported_t1_x = Column(Float)
    reported_t1_y = Column(Float)

    test_summary_id = Column(Integer, ForeignKey("test_summary.id"))

    test = relationship("TestSummary", back_populates="test_runs")
