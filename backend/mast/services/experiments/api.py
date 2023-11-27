from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from mast.services.experiments import service, schemas
from mast.database import get_db

router = APIRouter()

@router.get("/references/", response_model=list[schemas.Reference])
def read_references(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    refs = service.get_references(db, skip=skip, limit=limit)
    return refs

@router.get("/references/{reference_id}", response_model=schemas.Reference)
def read_reference(reference_id: int, db: Session = Depends(get_db)):
    db_ref = service.get_reference(db, reference_id=reference_id)
    if db_ref is None:
        raise HTTPException(status_code=404, detail="Reference not found")
    return db_ref

@router.post("/experiments",
             status_code=200,
             description="-- Experiments --"
             )
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    return service.create_experiment(db=db, experiment=experiment)

@router.get("/experiments/", response_model=list[schemas.Experiment])
def read_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiments = service.get_experiments(db, skip=skip, limit=limit)
    return experiments

@router.get("/experiments/{experiment_id}", response_model=schemas.Experiment)
def read_experiment(experiment_id: int, db: Session = Depends(get_db)):
    db_experiment = service.get_experiment(db, experiment_id=experiment_id)
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return db_experiment

@router.get("/experiments/{experiment_id}/run_results/", response_model=list[schemas.RunResult])
def get_run_results_by_experiment(
    experiment_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return service.get_run_results_by_experiment(db=db, experiment_id=experiment_id)

@router.post("/experiments/{experiment_id}/run_results/", response_model=schemas.RunResult)
def create_run_result_for_experiment(
    experiment_id: int, run_result: schemas.RunResultCreate, db: Session = Depends(get_db)
):
    return service.create_experiment_run_result(db=db, run_result=run_result, experiment_id=experiment_id)

@router.get("/run_results/", response_model=list[schemas.RunResult])
def read_run_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    run_results = service.get_run_results(db, skip=skip, limit=limit)
    return run_results