from fastapi import Depends, Security, APIRouter, Query, Response, Body

from app.db import get_session, AsyncSession
from app.services.analysis.models import Counts
from app.services.experiments.service import ExperimentsService
from app.services.references.service import ReferencesService
from app.services.runresults.service import RunResultsService
from app.services.experiments.models import ExperimentFrequencies, ExperimentParallelCount
from app.services.runresults.models import RunResultVulnerability, RunResultFragility

router = APIRouter()


@router.get("/counts", response_model=Counts)
async def get_general_counts(
    session: AsyncSession = Depends(get_session),
) -> Counts:
    """Get some counts about the database"""
    exp_service = ExperimentsService(session)
    exp_count = await exp_service.count()
    mod_count = await exp_service.count(True)
    ref_service = ReferencesService(session)
    ref_count = await ref_service.count()
    runres_service = RunResultsService(session)
    runres_count = await runres_service.count()
    return Counts(experiments_count=exp_count, models_count=mod_count, references_count=ref_count, run_results_count=runres_count)


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

    # case no filter
    if filter == "{}" or not filter:
        return res

    # case with filter, mark selected ones
    resAll = await service.parallel_count({})
    for parCountAll in resAll:
        # find parCount in resAll
        for parCount in res:
            if parCountAll.masonry_unit_material == parCount.masonry_unit_material and \
                    parCountAll.masonry_unit_type == parCount.masonry_unit_type and \
                    parCountAll.diaphragm_material == parCount.diaphragm_material and \
                    parCountAll.wall_leaves_nb == parCount.wall_leaves_nb and \
                    parCountAll.storeys_nb == parCount.storeys_nb and \
                    parCountAll.test_scale == parCount.test_scale and \
                    parCountAll.simultaneous_excitations_nb == parCount.simultaneous_excitations_nb and \
                    parCountAll.retrofitting_application == parCount.retrofitting_application and \
                    parCountAll.model_files == parCountAll.model_files:
                parCountAll.selected = True
                break
    return resAll


@router.get("/run_results/vulnerabilities", response_model=list[RunResultVulnerability])
async def get_run_results_vulnerability(
    response: Response,
    filter: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[RunResultVulnerability]:
    """Get the vulnerability of the run results, PGA vs. DG"""
    service = RunResultsService(session)
    res = await service.vulnerability(filter)

    return res


@router.get("/run_results/fragilities", response_model=list[RunResultFragility])
async def get_run_results_fragilities(
    response: Response,
    filter: str = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[RunResultVulnerability]:
    """Get the vulnerability of the run results, PGA vs. DG"""
    service = RunResultsService(session)
    vulnerabilities = await service.vulnerability(filter)
    fragilities = service.fragility(vulnerabilities)

    return fragilities
