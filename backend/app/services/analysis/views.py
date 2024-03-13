from fastapi import Depends, Security, APIRouter, Query, Response, Body

from app.db import get_session, AsyncSession
from app.services.analysis.models import Metrics
from app.services.experiments.service import ExperimentsService
from app.services.references.service import ReferencesService
from app.services.runresults.service import RunResultsService

router = APIRouter()


@router.get("/metrics", response_model=Metrics)
async def get_metrics(
    session: AsyncSession = Depends(get_session),
) -> Metrics:
    """Get some metrics about the database"""
    exp_service = ExperimentsService(session)
    exp_count = await exp_service.count()
    ref_service = ReferencesService(session)
    ref_count = await ref_service.count()
    runres_service = RunResultsService(session)
    runres_count = await runres_service.count()
    return Metrics(experiments_count=exp_count, references_count=ref_count, run_results_count=runres_count)
