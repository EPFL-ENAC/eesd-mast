from fastapi import Depends, Security, APIRouter, Query, Response, Body
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.references.models import (
    Reference,
    ReferenceCreate,
    ReferenceRead,
    ReferenceUpdate,
)
from app.services.references.service import ReferencesService

router = APIRouter()


@router.get("/{reference_id}", response_model=ReferenceRead)
async def get_reference(
    session: AsyncSession = Depends(get_session),
    *,
    reference_id: int | str,
) -> ReferenceRead:
    """Get a reference by id or short name"""
    service = ReferencesService(session)
    reference = await service.get(reference_id)
    return reference


@router.get("", response_model=list[ReferenceRead])
async def get_references(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[ReferenceRead]:
    """Get all references"""
    service = ReferencesService(session)
    start, end, total_count, references = await service.find(filter, sort, range)

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
    service = ReferencesService(session)
    reference = await service.create(Reference.from_orm(reference))
    return reference


@router.put("/{reference_id}", response_model=ReferenceRead)
async def update_reference(
    reference_id: int,
    reference_update: ReferenceUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> ReferenceRead:
    service = ReferencesService(session)
    reference = await service.patch(reference_id, reference_update)
    return reference


@router.delete("/{reference_id}")
async def delete_reference(
    reference_id: int,
    recursive: bool = Query(None),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete an reference by id"""
    service = ReferencesService(session)
    await service.delete(reference_id, recursive)
