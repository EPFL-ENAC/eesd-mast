from fastapi import Depends, Security, APIRouter, Query, Response, Body, HTTPException
from sqlmodel import select
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.experiments.models import (
    Experiment,
    ExperimentCreate,
    ExperimentRead,
    ExperimentUpdate,
)
from app.utils.query import QueryBuilder
from logging import debug

router = APIRouter()


@router.get("/{experiment_id}", response_model=ExperimentRead)
async def get_experiment(
    session: AsyncSession = Depends(get_session),
    *,
    experiment_id: int,
) -> ExperimentRead:
    """Get an experiment by id"""
    res = await session.exec(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment = res.one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return experiment


@router.get("", response_model=list[ExperimentRead])
async def get_experiments(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
):
    """Get all experiments"""

    builder = QueryBuilder(Experiment, filter, sort, range)

    # Do a query to satisfy total count for "Content-Range" header
    count_query = builder.build_count_query()
    total_count_query = await session.exec(count_query)
    total_count = total_count_query.one()

    # Main query
    start, end, query = builder.build_query(total_count)

    # Execute query
    results = await session.exec(query)
    references = results.all()

    # Execute query
    results = await session.exec(query)
    experiments = results.all()

    response.headers[
        "Content-Range"
    ] = f"experiments {start}-{end}/{total_count}"
    return experiments


@router.post("", response_model=ExperimentRead)
async def create_experiment(
    experiment: ExperimentCreate = Body(...),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> ExperimentRead:
    """Creates an experiment"""
    experiment = Experiment.from_orm(experiment)
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)

    return experiment


@router.put("/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(
    experiment_id: int,
    experiment_update: ExperimentUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> ExperimentRead:
    res = await session.exec(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment_db = res.one()
    experiment_data = experiment_update.dict(exclude_unset=True)

    if not experiment_db:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Update the fields from the request
    for field, value in experiment_data.items():
        debug(f"Updating: {field}, {value}")
        setattr(experiment_db, field, value)

    session.add(experiment_db)
    await session.commit()
    await session.refresh(experiment_db)

    return experiment_db


@router.delete("/{experiment_id}")
async def delete_experiment(
    experiment_id: int,
    session: AsyncSession = Depends(get_session),
    filter: dict[str, str] | None = None,
    api_key: str = Security(get_api_key),
) -> None:
    """Delete an experiment by id"""
    res = await session.exec(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment = res.one_or_none()

    if experiment:
        await session.delete(experiment)
        await session.commit()