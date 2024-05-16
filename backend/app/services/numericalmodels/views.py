
from fastapi import Depends, Security, APIRouter, Query, Response, Body
from app.db import get_session, AsyncSession
from app.auth import get_api_key
from app.services.numericalmodels.service import NumericalModelsService
from app.services.numericalmodels.models import (
    NumericalModel,
    NumericalModelCreate,
    NumericalModelRead,
    NumericalModelUpdate,
)
from logging import debug

router = APIRouter()


@router.get("/{numerical_model_id}", response_model=NumericalModelRead)
async def get_numerical_model(
    session: AsyncSession = Depends(get_session),
    *,
    numerical_model_id: int,
) -> NumericalModelRead:
    """Get a numerical model by id"""
    service = NumericalModelsService(session)
    numerical_model = await service.get(numerical_model_id)
    return numerical_model


@router.get("", response_model=list[NumericalModelRead])
async def get_numerical_models(
    response: Response,
    filter: str = Query(None),
    sort: str = Query(None),
    range: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[NumericalModelRead]:
    """Get all numerical models"""
    service = NumericalModelsService(session)
    start, end, total_count, numerical_models = await service.find(filter, sort, range)

    response.headers[
        "Content-Range"
    ] = f"numerical_models {start}-{end}/{total_count}"
    return numerical_models


@router.post("", response_model=NumericalModelRead)
async def create_numerical_model(
    numerical_model: NumericalModelCreate = Body(...),
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> NumericalModelRead:
    """Create a numerical model"""
    service = NumericalModelsService(session)
    numerical_model = await service.create(NumericalModel.model_validate(numerical_model))
    return numerical_model


@router.put("/{numerical_model_id}", response_model=NumericalModelRead)
async def update_numerical_model(
    numerical_model_id: int,
    numerical_model_update: NumericalModelUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key)
) -> NumericalModelRead:
    """Update a numerical model"""
    service = NumericalModelsService(session)
    numerical_model = await service.patch(numerical_model_id, numerical_model_update)
    return numerical_model


@router.delete("/{numerical_model_id}")
async def delete_numerical_model(
    numerical_model_id: int,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(get_api_key),
) -> None:
    """Delete a numerical model by id"""
    service = NumericalModelsService(session)
    service.delete(numerical_model_id)
