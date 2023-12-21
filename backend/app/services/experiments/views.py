from fastapi import Depends, Security, APIRouter, Query, Response, Body
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.experiments.service import ExperimentsService
from app.services.experiments.models import (
    Experiment,
    ExperimentCreate,
    ExperimentRead,
    ExperimentUpdate,
)

router = APIRouter()


@router.get("/{experiment_id}", response_model=ExperimentRead)
async def get_experiment(
    session: AsyncSession = Depends(get_session),
    *,
    experiment_id: int,
) -> ExperimentRead:
    """Get an experiment by id"""
    service = ExperimentsService(session)
    experiment = await service.get(experiment_id)
    return experiment


@router.get("", response_model=list[ExperimentRead])
async def get_experiments(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[ExperimentRead]:
    """Get all experiments"""
    service = ExperimentsService(session)
    start, end, total_count, experiments = await service.find(filter, sort, range)

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
    service = ExperimentsService(session)
    experiment = await service.create(Experiment.from_orm(experiment))
    return experiment


@router.put("/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(
    experiment_id: int,
    experiment_update: ExperimentUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> ExperimentRead:
    """Update an experiment by id"""
    service = ExperimentsService(session)
    experiment = await service.patch(experiment_id, experiment_update)
    return experiment


@router.delete("/{experiment_id}")
async def delete_experiment(
    experiment_id: int,
    recursive: bool = Query(None),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete an experiment by id"""
    service = ExperimentsService(session)
    await service.delete(experiment_id, recursive)
