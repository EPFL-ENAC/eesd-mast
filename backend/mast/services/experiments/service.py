from sqlalchemy.orm import Session
from mast.services.experiments import models, schemas

# Experiments

def get_experiment(db: Session, experiment_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()

def get_experiments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Experiment).offset(skip).limit(limit).all()

def get_experiments_by_reference(db: Session, reference_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Experiment).filter(models.Experiment.reference_id == reference_id).offset(skip).limit(limit).all()

def create_experiment(db: Session, experiment: models.Experiment):
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment

def delete_experiment(db: Session, experiment_id: int):
    delete_experiment_run_results(db, experiment_id)
    db.query(models.Experiment).filter(models.Experiment.id == experiment_id).delete()
    db.commit()

def delete_reference_experiments(db: Session, reference_id: int):
    db.query(models.Experiment).filter(models.Experiment.reference_id == reference_id).delete()
    db.commit()

# Run results

def get_run_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RunResult).offset(skip).limit(limit).all()

def get_run_results_by_experiment(db: Session, experiment_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.RunResult).filter(models.RunResult.experiment_id == experiment_id).offset(skip).limit(limit).all()

def create_experiment_run_result(db: Session, run_result: models.RunResult):
    db.add(run_result)
    db.commit()
    db.refresh(run_result)
    return run_result

def delete_run_result(db: Session, run_result_id: int):
    db.query(models.RunResult).filter(models.RunResult.id == run_result_id).delete()
    db.commit()

def delete_experiment_run_results(db: Session, experiment_id: int):
    db.query(models.RunResult).filter(models.RunResult.experiment_id == experiment_id).delete()
    db.commit()