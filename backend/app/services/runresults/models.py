from sqlmodel import SQLModel, Field, UniqueConstraint
from pydantic import BaseModel


class RunResultBase(SQLModel):
    run_id: str = Field(unique=True, index=True)
    nominal_pga_x: float | None
    nominal_pga_y: float | None
    nominal_pga_z: float | None
    actual_pga_x: float | None
    actual_pga_y: float | None
    actual_pga_z: float | None
    dg_reported: float | None
    dg_derived: float | None
    max_top_drift_x: float | None
    max_top_drift_y: float | None
    residual_top_drift_x: float | None
    residual_top_drift_y: float | None
    base_shear_coef: float | None
    reported_t1_x: float | None
    reported_t1_y: float | None

    experiment_id: int = Field(
        default=None, foreign_key="experiment.id", index=True
    )


class RunResult(RunResultBase, table=True):
    __table_args__ = (UniqueConstraint("id"),)
    id: int = Field(
        default=None,
        nullable=False,
        primary_key=True,
        index=True,
    )


class RunResultRead(RunResultBase):
    id: int


class RunResultCreate(RunResultBase):
    pass


class RunResultUpdate(RunResultBase):
    pass


class RunResultVulnerability(BaseModel):
    pgas: list[float] | None
    dg: int | None


class RunResultFragility(BaseModel):
    thresh: list[float] | None
    prob: list[float] | None
    x: list[float] | None
    y: list[float] | None
    dg: int | None
