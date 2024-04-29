from app.services.runresults.models import RunResult, RunResultUpdate, RunResultVulnerability
from app.services.experiments.models import Experiment
from app.utils.query import QueryBuilder
from sqlmodel import select, join, not_
from sqlalchemy.sql import text
from fastapi import HTTPException
from app.db import AsyncSession


class RunResultsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self) -> int:
        """Count all run results"""
        count = (await self.session.exec(text("select count(id) from runresult"))).scalar()
        return count

    async def vulnerability(self, filter: dict | str) -> list[RunResultVulnerability]:
        """Get vulnerabilities from all run results"""
        query = select(RunResult.nominal_pga_x, RunResult.nominal_pga_y, RunResult.dg_derived, RunResult.dg_reported) \
            .select_from(join(RunResult, Experiment)) \
            .where(RunResult.nominal_pga_x.isnot(None) | RunResult.nominal_pga_y.isnot(None)) \
            .where(RunResult.dg_derived.isnot(None) | RunResult.dg_reported.isnot(None)) \
            .where(not_(RunResult.run_id.in_(['Initial', 'Final'])))

        builder = QueryBuilder(Experiment, filter, [], [])
        query = builder.build_filter_query(query)

        # Execute query
        results = await self.session.exec(query)
        vulnerabilities = []
        for result in results.all():
            vulnerability = RunResultVulnerability(
                pga=result.nominal_pga_x if result.nominal_pga_x else result.nominal_pga_y,
                dg=result.dg_derived if result.dg_derived else result.dg_reported,
            )
            vulnerabilities.append(vulnerability)

        return vulnerabilities

    async def get(self, run_result_id: int) -> RunResult:
        """Get a run result by id"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result = res.one_or_none()
        if not run_result:
            raise HTTPException(status_code=404, detail="Run result not found")

        return run_result

    async def find(self, filter: dict | str, sort: list | str, range: list | str) -> list[int, int, int, RunResult]:
        """Get all run results matching filter and range"""
        builder = QueryBuilder(RunResult, filter, sort, range)

        # Do a query to satisfy total count for "Content-Range" header
        count_query = builder.build_count_query()
        total_count_query = await self.session.exec(count_query)
        total_count = total_count_query.one()

        # Main query
        start, end, query = builder.build_query(total_count)

        # Execute query
        results = await self.session.exec(query)
        run_results = results.all()

        return [start, end, total_count, run_results]

    async def create(self, run_result: RunResult) -> RunResult:
        """Create a run result"""
        self.session.add(run_result)
        await self.session.commit()
        await self.session.refresh(run_result)
        return run_result

    async def patch(self, run_result_id: int, run_result: RunResultUpdate) -> RunResult:
        """Update a run result"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result_db = res.one()
        run_result_data = run_result.dict(exclude_unset=True)

        if not run_result_db:
            raise HTTPException(status_code=404, detail="Run result not found")

        # Update the fields from the request
        for field, value in run_result_data.items():
            setattr(run_result_db, field, value)

        self.session.add(run_result_db)
        await self.session.commit()
        await self.session.refresh(run_result_db)
        return run_result_db

    async def delete(self, run_result_id: int) -> None:
        """Delete a run result by id"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result = res.one_or_none()

        if run_result:
            await self.session.delete(run_result)
            await self.session.commit()

    async def delete_by_experiment(self, experiment_id: int) -> None:
        """Delete all run results by experiment id"""
        start, stop, total_count, run_results = await self.find(filter={"experiment_id": experiment_id}, sort=None, range=None)
        if run_results:
            [await self.session.delete(run_result) for run_result in run_results]
            await self.session.commit()
