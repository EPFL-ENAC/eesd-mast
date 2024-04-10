from fastapi import Depends, Security, APIRouter, Query, Response, Body

from app.db import get_session, AsyncSession
from app.services.analysis.models import Counts
from app.services.experiments.service import ExperimentsService
from app.services.references.service import ReferencesService
from app.services.runresults.service import RunResultsService
from app.services.experiments.models import ExperimentFrequencies, ExperimentParallelCount

router = APIRouter()


@router.get("/counts", response_model=Counts)
async def get_general_counts(
    session: AsyncSession = Depends(get_session),
) -> Counts:
    """Get some counts about the database"""
    exp_service = ExperimentsService(session)
    exp_count = await exp_service.count()
    ref_service = ReferencesService(session)
    ref_count = await ref_service.count()
    runres_service = RunResultsService(session)
    runres_count = await runres_service.count()
    return Counts(experiments_count=exp_count, references_count=ref_count, run_results_count=runres_count)


@router.get("/experiments/frequencies", response_model=ExperimentFrequencies)
async def get_experiments_frequencies(
    response: Response,
    filter: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> ExperimentFrequencies:
    """Get the frequency of some fields in the experiments"""
    service = ExperimentsService(session)
    res = await service.frequencies(filter)
    return res


@router.get("/experiments/parallel-counts", response_model=list[ExperimentParallelCount])
async def get_experiments_parallel_counts(
    response: Response,
    filter: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[ExperimentParallelCount]:
    """Get the count of some fields in the experiments"""
    service = ExperimentsService(session)
    res = await service.parallel_count(filter)
    return res
