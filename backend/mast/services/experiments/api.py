from fastapi import Depends, Security, APIRouter, HTTPException
from sqlalchemy.orm import Session

from mast.services.experiments import service, schemas, models
from mast.database import get_db
from mast.auth import get_api_key

router = APIRouter()

@router.post("/experiments",
             status_code=200,
             description="-- Experiments --"
             )
def create_experiment(
    reference_id: int, experiment: schemas.ExperimentCreate, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    db_exp = models.Experiment(**experiment.dict(), reference_id=reference_id)
    return service.create_experiment(db=db, experiment=db_exp)

@router.get("/experiments/", response_model=list[schemas.Experiment])
def read_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiments = service.get_experiments(db, skip=skip, limit=limit)
    return experiments

@router.get("/references/{reference_id}/experiments/", response_model=list[schemas.Experiment])
def read_experiments_by_reference(reference_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiments = service.get_experiments_by_reference(db, reference_id=reference_id, skip=skip, limit=limit)
    return experiments

@router.get("/experiments/{experiment_id}", response_model=schemas.Experiment)
def read_experiment(experiment_id: int, db: Session = Depends(get_db)):
    db_experiment = service.get_experiment(db, experiment_id=experiment_id)
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return db_experiment

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    service.delete_experiment(db, experiment_id=experiment_id)

@router.get("/experiments/{experiment_id}/run_results/", response_model=list[schemas.RunResult])
def get_run_results_by_experiment(
    experiment_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_run_results_by_experiment(db=db, experiment_id=experiment_id, skip=skip, limit=limit)

@router.post("/experiments/{experiment_id}/run_results/", response_model=schemas.RunResult)
def create_experiment_run_result(
    experiment_id: int, run_result: schemas.RunResultCreate, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    db_run = models.RunResult(**run_result.dict(), experiment_id=experiment_id)
    return service.create_experiment_run_result(db=db, run_result=db_run)

@router.delete("/experiments/{experiment_id}/run_results/")
def delete_experiment_run_results(
    experiment_id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    service.delete_experiment_run_results(db, experiment_id=experiment_id)

@router.get("/run_results/", response_model=list[schemas.RunResult])
def read_run_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    run_results = service.get_run_results(db, skip=skip, limit=limit)
    return run_results