from app.services.experiments.models import Experiment, ExperimentRead, ExperimentUpdate, ExperimentFrequencies, ExperimentParallelCount, ExperimentCounts
from app.services.references.models import Reference, ReferenceRead
from app.services.runresults.service import RunResultsService
from app.services.runresults.models import RunResult
from app.services.numericalmodels.service import NumericalModelsService
from app.services.numericalmodels.models import NumericalModel
from app.services.files.s3client import s3_client
from app.utils.query import QueryBuilder
from sqlmodel import select
from sqlalchemy.sql import text
from fastapi import HTTPException
from app.db import AsyncSession


class ExperimentsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self, withModel: bool = None) -> int:
        """Count all experiments"""
        if withModel:
            return (await self.session.exec(text("select count(id) from experiment where cast(model_files as varchar) != 'null' and model_files is not null"))).scalar()
        return (await self.session.exec(text("select count(id) from experiment"))).scalar()

    async def frequencies(self, filter: dict | str) -> ExperimentFrequencies:
        """Get aggregations for the experiments matching filter"""
        field_counts = {}
        for field in ["masonry_unit_material", "diaphragm_material", "storeys_nb", "test_scale"]:
            builder = QueryBuilder(Experiment, filter, [], [])
            query = builder.build_frequencies_query(field)
            results = await self.session.exec(query)
            rows = results.fetchall()
            # exclude 0 counts
            counts = {row[0]: row[1] for row in rows if row[1] != 0}
            field_counts[field] = counts

        for field in ["model_files"]:
            builder = QueryBuilder(Experiment, filter, [], [])
            query = builder.build_frequencies_exists_query(field)
            results = await self.session.exec(query)
            rows = results.fetchall()
            print(rows)
            # exclude 0 counts
            counts = {row[0]: row[1] for row in rows if row[1] != 0}
            field_counts[field] = counts

        return ExperimentFrequencies(**field_counts)

    async def parallel_count(self, filter: dict | str) -> list[ExperimentParallelCount]:
        """Get aggregations for the experiments matching filter"""
        fields = ["masonry_unit_material", "masonry_unit_type",
                  "diaphragm_material", "wall_leaves_nb", "storeys_nb",
                  "test_scale", "simultaneous_excitations_nb", "retrofitting_application", "with_model"]
        builder = QueryBuilder(ExperimentCounts, filter, [], [])
        query = builder.build_parallel_count_query(fields)
        results = await self.session.exec(query)
        rows = results.fetchall()

        return [ExperimentParallelCount(**dict(zip(fields + ["count"], row))) for row in rows]

    async def get(self, experiment_id: int) -> ExperimentRead:
        """Get an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        experiment = ExperimentRead.model_validate(experiment)

        # Get reference
        res = await self.session.exec(
            select(Reference).where(
                Reference.id == experiment.reference_id)
        )
        reference = res.one_or_none()
        reference_reference = ReferenceRead.model_validate(reference)

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
        experiments = [ExperimentRead.model_validate(
            experiment) for experiment in experiments]

        # Reference IDs
        reference_ids = [experiment.reference_id for experiment in experiments]
        res = await self.session.exec(
            select(Reference).where(
                Reference.id.in_(reference_ids))
        )
        references = res.all()
        reference_dict = {
            reference.id: reference for reference in references}

        # Add reference short name to each experiment
        for experiment in experiments:
            experiment.reference = ReferenceRead.model_validate(
                reference_dict[experiment.reference_id])

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
            if experiment.plan_files:
                key = experiment.plan_files['name']
                await s3_client.delete_files(f"experiments/{experiment_id}/{key}")
            if experiment.model_files:
                key = experiment.model_files['name']
                await s3_client.delete_files(f"experiments/{experiment_id}/{key}")
            if experiment.test_files:
                key = experiment.test_files['name']
                await s3_client.delete_files(f"experiments/{experiment_id}/{key}")
            # Delete run results and numerical models
            if recursive:
                run_results_service = RunResultsService(self.session)
                await run_results_service.delete_by_experiment(experiment_id)
                numerical_models_service = NumericalModelsService(self.session)
                await numerical_models_service.delete_by_experiment(experiment_id)
            # Delete experiment
            await self.session.delete(experiment)
            await self.session.commit()

        return experiment

    async def get_run_results(self, experiment_id: int) -> list[RunResult]:
        """Delete run results of an experiment by id"""
        run_results_service = RunResultsService(self.session)
        return await run_results_service.get_by_experiment(experiment_id)

    async def delete_run_results(self, experiment_id: int) -> None:
        """Delete run results of an experiment by id"""
        run_results_service = RunResultsService(self.session)
        await run_results_service.delete_by_experiment(experiment_id)

    async def get_numerical_model(self, experiment_id: int) -> NumericalModel:
        """Get numerical model of an experiment by id"""
        numerical_models_service = NumericalModelsService(self.session)
        return await numerical_models_service.get_by_experiment(experiment_id)

    async def delete_numerical_model(self, experiment_id: int) -> None:
        """Delete numerical model of an experiment by id"""
        numerical_models_service = NumericalModelsService(self.session)
        await numerical_models_service.delete_by_experiment(experiment_id)

    async def delete_scheme_file(self, experiment_id: int) -> None:
        """Delete scheme file of an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment and experiment.scheme:
            name = experiment.scheme['name']
            s3_file = f"experiments/{experiment_id}/{name}"
            deleted = await s3_client.delete_file(s3_file)
            if deleted:
                experiment.scheme = None
                await self.session.commit()

    async def delete_plan_files(self, experiment_id: int) -> None:
        """Delete plan files of an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment and experiment.plan_files:
            key = experiment.plan_files['name']
            s3_folder = f"experiments/{experiment_id}/{key}"
            deleted = await s3_client.delete_files(s3_folder)
            if deleted:
                experiment.plan_files = None
                await self.session.commit()

    async def delete_model_files(self, experiment_id: int) -> None:
        """Delete numerical model files of an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment and experiment.model_files:
            key = experiment.model_files['name']
            s3_folder = f"experiments/{experiment_id}/{key}"
            deleted = await s3_client.delete_files(s3_folder)
            if deleted:
                experiment.model_files = None
                await self.session.commit()

    async def delete_test_files(self, experiment_id: int) -> None:
        """Delete files of an experiment by id"""
        res = await self.session.exec(
            select(Experiment).where(Experiment.id == experiment_id)
        )
        experiment = res.one_or_none()

        if experiment and experiment.test_files:
            key = experiment.test_files['name']
            s3_folder = f"experiments/{experiment_id}/{key}"
            deleted = await s3_client.delete_files(s3_folder)
            if deleted:
                experiment.test_files = None
                await self.session.commit()

    async def delete_by_reference(self, reference_id: int, recursive: bool = False) -> None:
        """Delete all experiments by reference id"""
        start, stop, total_count, experiments = await self.find(filter={"reference_id": reference_id}, sort=None, range=None)
        if experiments:
            [await self.delete(experiment.id, recursive) for experiment in experiments]
