
from fastapi import Depends, Security, APIRouter, Query, Response, Body, HTTPException
from sqlmodel import select
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.runresults.service import RunResultsService
from app.services.runresults.models import (
    RunResult,
    RunResultCreate,
    RunResultRead,
    RunResultUpdate,
)
from app.utils.query import QueryBuilder
from logging import debug

router = APIRouter()


@router.get("/{run_result_id}", response_model=RunResultRead)
async def get_run_result(
    session: AsyncSession = Depends(get_session),
    *,
    run_result_id: int,
) -> RunResultRead:
    """Get a run result by id"""
    service = RunResultsService(session)
    run_result = await service.get(run_result_id)
    return run_result


@router.get("", response_model=list[RunResultRead])
async def get_run_results(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[RunResultRead]:
    """Get all run results"""
    service = RunResultsService(session)
    start, end, total_count, run_results = await service.find(filter, sort, range)

    response.headers[
        "Content-Range"
    ] = f"run_results {start}-{end}/{total_count}"
    return run_results


@router.post("", response_model=RunResultRead)
async def create_run_result(
    run_result: RunResultCreate = Body(...),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> RunResultRead:
    """Creates a run result"""
    service = RunResultsService(session)
    run_result = await service.create(RunResult.from_orm(run_result))
    return run_result


@router.put("/{run_result_id}", response_model=RunResultRead)
async def update_run_result(
    run_result_id: int,
    run_result_update: RunResultUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> RunResultRead:
    service = RunResultsService(session)
    run_result = await service.patch(run_result_id, run_result_update)
    return run_result


@router.delete("/{run_result_id}")
async def delete_run_result(
    run_result_id: int,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete a run result by id"""
    service = RunResultsService(session)
    service.delete(run_result_id)
