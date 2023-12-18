
from fastapi import Depends, Security, APIRouter, Query, Response, Body, HTTPException
from sqlmodel import select
from app.db import get_session, AsyncSession
from app.auth import get_api_key
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
    res = await session.exec(
        select(RunResult).where(RunResult.id == run_result_id)
    )
    run_result = res.one_or_none()
    if not run_result:
        raise HTTPException(status_code=404, detail="RunResult not found")

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

    builder = QueryBuilder(RunResult, filter, sort, range)

    # Do a query to satisfy total count for "Content-Range" header
    count_query = builder.build_count_query()
    total_count_query = await session.exec(count_query)
    total_count = total_count_query.one()

    # Main query
    start, end, query = builder.build_query(total_count)

    # Execute query
    results = await session.exec(query)
    run_results = results.all()

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
    run_result = RunResult.from_orm(run_result)
    session.add(run_result)
    await session.commit()
    await session.refresh(run_result)

    return run_result


@router.put("/{run_result_id}", response_model=RunResultRead)
async def update_run_result(
    run_result_id: int,
    run_result_update: RunResultUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> RunResultRead:
    res = await session.exec(
        select(RunResult).where(RunResult.id == run_result_id)
    )
    run_result_db = res.one()
    run_result_data = run_result_update.dict(exclude_unset=True)

    if not run_result_db:
        raise HTTPException(status_code=404, detail="RunResult not found")

    # Update the fields from the request
    for field, value in run_result_data.items():
        debug(f"Updating: {field}, {value}")
        setattr(run_result_db, field, value)

    session.add(run_result_db)
    await session.commit()
    await session.refresh(run_result_db)

    return run_result_db


@router.delete("/{run_result_id}")
async def delete_run_result(
    run_result_id: int,
    session: AsyncSession = Depends(get_session),
    filter: dict[str, str] | None = None,
    api_key: str = Security(get_api_key),
) -> None:
    """Delete a run result by id"""
    res = await session.exec(
        select(RunResult).where(RunResult.id == run_result_id)
    )
    run_result = res.one_or_none()

    if run_result:
        await session.delete(run_result)
        await session.commit()