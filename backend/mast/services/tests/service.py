from sqlalchemy.orm import Session
from mast.services.tests import models, schemas

def get_experiment(db: Session, experiment_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()

def get_experiment_by_author_email(db: Session, email: str):
    return db.query(models.Experiment).filter(models.Experiment.corresponding_author_email == email).first()

def get_experiments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Experiment).offset(skip).limit(limit).all()

def create_experiment(db: Session, experiment: schemas.ExperimentCreate):
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment

def get_run_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RunResult).offset(skip).limit(limit).all()

def create_experiment_run_result(db: Session, run_result: schemas.RunResultCreate, experiment_id: int):
    db_run_result = models.RunResult(**run_result.model_dump(), experiment_id=experiment_id)
    db.add(db_run_result)
    db.commit()
    db.refresh(db_run_result)
    return db_run_result
