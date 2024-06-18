from app.services.numericalmodels.models import NumericalModel, NumericalModelUpdate
from app.services.experiments.models import Experiment
from app.utils.query import QueryBuilder
from sqlmodel import select, join, not_
from sqlalchemy.sql import text
from fastapi import HTTPException
from app.db import AsyncSession
from scipy.stats import lognorm
import statsmodels.api as sm
import numpy as np


class NumericalModelsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self) -> int:
        """Count all numerical models"""
        count = (await self.session.exec(text("select count(id) from numericalmodel"))).scalar()
        return count

    async def get(self, numerical_model_id: int) -> NumericalModel:
        """Get a numerical model by id"""
        res = await self.session.exec(
            select(NumericalModel).where(
                NumericalModel.id == numerical_model_id)
        )
        numerical_model = res.one_or_none()
        if not numerical_model:
            raise HTTPException(
                status_code=404, detail="Numerical model not found")

        return numerical_model

    async def find(self, filter: dict | str, sort: list | str, range: list | str) -> list[int, int, int, NumericalModel]:
        """Get all numerical models matching filter and range"""
        builder = QueryBuilder(NumericalModel, filter, sort, range)

        # Do a query to satisfy total count for "Content-Range" header
        count_query = builder.build_count_query()
        total_count_query = await self.session.exec(count_query)
        total_count = total_count_query.one()

        # Main query
        start, end, query = builder.build_query(total_count)

        # Execute query
        results = await self.session.exec(query)
        numerical_models = results.all()

        return [start, end, total_count, numerical_models]

    async def get_by_experiment(self, experiment_id: int) -> NumericalModel:
        start, stop, total_count, numerical_models = await self.find(filter={"experiment_id": experiment_id}, sort=None, range=None)
        if numerical_models:
            return numerical_models[0]
        else:
            raise HTTPException(
                status_code=404, detail="Numerical model not found")

    async def create(self, numerical_model: NumericalModel) -> NumericalModel:
        """Create a numerical model"""
        self.session.add(numerical_model)
        await self.session.commit()
        await self.session.refresh(numerical_model)
        return numerical_model

    async def patch(self, numerical_model_id: int, numerical_model: NumericalModelUpdate) -> NumericalModel:
        """Update a numerical model"""
        res = await self.session.exec(
            select(NumericalModel).where(
                NumericalModel.id == numerical_model_id)
        )
        numerical_model_db = res.one()
        numerical_model_data = numerical_model.dict(exclude_unset=True)

        if not numerical_model_db:
            raise HTTPException(
                status_code=404, detail="Numerical model not found")

        # Update the fields from the request
        for field, value in numerical_model_data.items():
            setattr(numerical_model_db, field, value)

        self.session.add(numerical_model_db)
        await self.session.commit()
        await self.session.refresh(numerical_model_db)
        return numerical_model_db

    async def delete(self, numerical_model_id: int) -> None:
        """Delete a numerical model by id"""
        res = await self.session.exec(
            select(NumericalModel).where(
                NumericalModel.id == numerical_model_id)
        )
        numerical_model = res.one_or_none()

        if numerical_model:
            await self.session.delete(numerical_model)
            await self.session.commit()

    async def delete_by_experiment(self, experiment_id: int) -> None:
        """Delete numerical model by experiment id"""
        start, stop, total_count, numerical_models = await self.find(filter={"experiment_id": experiment_id}, sort=None, range=None)
        if numerical_models:
            [await self.session.delete(numerical_model) for numerical_model in numerical_models]
            await self.session.commit()
