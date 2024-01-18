from app.services.experiments.models import Experiment, ExperimentRead, ExperimentUpdate
from app.services.references.models import Reference
from app.services.runresults.models import RunResult
from app.services.runresults.service import RunResultsService
from app.services.files.s3client import s3_client
from app.utils.query import QueryBuilder
from sqlmodel import select
from fastapi import HTTPException
from app.db import AsyncSession


class ExperimentsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, experiment_id: int) -> ExperimentRead:
        """Get an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        experiment = ExperimentRead.from_orm(experiment)

        # Get reference
        res = await self.session.exec(
            select(Reference.id, Reference.reference).where(
                Reference.id == experiment.reference_id)
        )
        reference = res.one_or_none()
        reference_reference = reference.reference if reference else None

        experiment.reference = reference_reference

        return experiment

    async def find(self, filter: dict | str, sort: list | str, range: list | str) -> list[int, int, int, ExperimentRead]:
        """Get all experiments matching filter and range"""
        builder = QueryBuilder(Experiment, filter, sort, range)

        # Do a query to satisfy total count for "Content-Range" header
        count_query = builder.build_count_query()
        total_count_query = await self.session.exec(count_query)
        total_count = total_count_query.one()

        # Main query
        start, end, query = builder.build_query(total_count)

        # Execute query
        results = await self.session.exec(query)
        experiments = results.all()
        # Cast to ExperimentRead
        experiments = [ExperimentRead.from_orm(
            experiment) for experiment in experiments]

        # Reference IDs
        reference_ids = [experiment.reference_id for experiment in experiments]
        res = await self.session.exec(
            select(Reference.id, Reference.reference).where(
                Reference.id.in_(reference_ids))
        )
        references = res.all()
        reference_dict = {
            reference.id: reference.reference for reference in references}

        # Add reference short name to each experiment
        for experiment in experiments:
            experiment.reference = reference_dict[experiment.reference_id]

        return [start, end, total_count, experiments]

    async def create(self, experiment: Experiment) -> Experiment:
        """Creates an experiment"""
        self.session.add(experiment)
        await self.session.commit()
        await self.session.refresh(experiment)
        return experiment

    async def patch(self, experiment_id: int, experiment: ExperimentUpdate) -> ExperimentRead:
        """Updates an experiment"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment_db = res.one_or_none()
        if not experiment_db:
            raise HTTPException(status_code=404, detail="Experiment not found")

        experiment_data = experiment.dict(exclude_unset=True)
        for field, value in experiment_data.items():
            setattr(experiment_db, field, value)

        await self.session.commit()
        await self.session.refresh(experiment_db)

        return experiment_db

    async def delete(self, experiment_id: int, recursive: bool = False) -> Experiment:
        """Delete an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment:
            # Delete associated files
            if experiment.scheme:
                await s3_client.delete_file(experiment.scheme['path'])
            if experiment.files:
                key = experiment.files['name']
                s3_folder = f"experiments/{experiment_id}/{key}"
                await s3_client.delete_files(s3_folder)
            # Delete run results
            if recursive:
                run_results_service = RunResultsService(self.session)
                await run_results_service.delete_by_experiment(experiment_id)
            # Delete experiment
            await self.session.delete(experiment)
            await self.session.commit()

        return experiment

    async def delete_files(self, experiment_id: int) -> None:
        """Delete files of an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment and experiment.files:
            if experiment.files:
                key = experiment.files['name']
                s3_folder = f"experiments/{experiment_id}/{key}"
                deleted = await s3_client.delete_files(s3_folder)
                if deleted:
                    experiment.files = None
                    await self.session.commit()

    async def delete_by_reference(self, reference_id: int, recursive: bool = False) -> None:
        """Delete all experiments by reference id"""
        start, stop, total_count, experiments = await self.find(filter={"reference_id": reference_id}, sort=None, range=None)
        if experiments:
            [await self.delete(experiment.id, recursive) for experiment in experiments]
