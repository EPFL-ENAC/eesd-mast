from fastapi import Depends, Security, APIRouter, Query, Response, Body, HTTPException
from sqlmodel import select
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.references.models import (
    Reference,
    ReferenceCreate,
    ReferenceRead,
    ReferenceUpdate,
)
from sqlalchemy import func
import json

router = APIRouter()

@router.get("/{reference_id}", response_model=ReferenceRead)
async def get_reference(
    session: AsyncSession = Depends(get_session),
    *,
    reference_id: int | str,
) -> ReferenceRead:
    """Get a reference by id or short name"""
    sel = select(Reference)
    if isinstance(reference_id, str):
        sel = sel.where(Reference.reference == reference_id)
    else:
        sel = sel.where(Reference.id == reference_id)
    res = await session.exec(sel)
    reference = res.one_or_none()
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")

    return reference


@router.get("", response_model=list[ReferenceRead])
async def get_references(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
):
    """Get all references"""

    sort = json.loads(sort) if sort else []
    range = json.loads(range) if range else []
    filter = json.loads(filter) if filter else {}

    query = select(Reference)

    # Do a query to satisfy total count for "Content-Range" header
    count_query = select(func.count(Reference.id))
    if len(filter):  # Have to filter twice for some reason? SQLModel state?
        for field, value in filter.items():
            for qry in [query, count_query]:  # Apply filter to both queries
                if isinstance(value, list):
                    qry = qry.where(getattr(Reference, field).in_(value))
                elif field == "id" or field == "reference_id":
                    qry = qry.where(getattr(Reference, field) == value)
                else:
                    qry = qry.where(
                        getattr(Reference, field).like(f"%{value}%")
                    )

    # Execute total count query (including filter)
    total_count_query = await session.exec(count_query)
    total_count = total_count_query.one()

    # Order by sort field params ie. ["name","ASC"]
    if len(sort) == 2:
        sort_field, sort_order = sort
        if sort_order == "ASC":
            query = query.order_by(getattr(Reference, sort_field))
        else:
            query = query.order_by(getattr(Reference, sort_field), getattr(Reference, sort_field).desc())

    # Filter by filter field params ie. {"name":"bar"}
    if len(filter):
        for field, value in filter.items():
            if isinstance(value, list):
                query = query.where(getattr(Reference, field).in_(value))
            elif field == "id" or field == "reference_id":
                query = query.where(getattr(Reference, field) == value)
            else:
                query = query.where(
                    getattr(Reference, field).like(f"%{value}%")
                )

    if len(range) == 2:
        start, end = range
        query = query.offset(start).limit(end - start + 1)
    else:
        start, end = [0, total_count]  # For content-range header

    # Execute query
    results = await session.exec(query)
    references = results.all()

    response.headers[
        "Content-Range"
    ] = f"references {start}-{end}/{total_count}"
    return references


@router.post("", response_model=ReferenceRead)
async def create_reference(
    reference: ReferenceCreate = Body(...),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> ReferenceRead:
    """Creates an reference"""
    print(reference)
    reference = Reference.from_orm(reference)
    session.add(reference)
    await session.commit()
    await session.refresh(reference)

    return reference


@router.put("/{reference_id}", response_model=ReferenceRead)
async def update_reference(
    reference_id: int,
    reference_update: ReferenceUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> ReferenceRead:
    res = await session.exec(
        select(Reference).where(Reference.id == reference_id)
    )
    reference_db = res.one()
    reference_data = reference_update.dict(exclude_unset=True)

    if not reference_db:
        raise HTTPException(status_code=404, detail="Reference not found")

    # Update the fields from the request
    for field, value in reference_data.items():
        print(f"Updating: {field}, {value}")
        setattr(reference_db, field, value)

    session.add(reference_db)
    await session.commit()
    await session.refresh(reference_db)

    return reference_db


@router.delete("/{reference_id}")
async def delete_reference(
    reference_id: int,
    session: AsyncSession = Depends(get_session),
    filter: dict[str, str] | None = None,
    api_key: str = Security(get_api_key),
) -> None:
    """Delete an reference by id"""
    res = await session.exec(
        select(Reference).where(Reference.id == reference_id)
    )
    reference = res.one_or_none()

    if reference:
        await session.delete(reference)
        await session.commit()