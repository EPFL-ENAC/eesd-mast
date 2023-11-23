from sqlalchemy.orm import Session
from mast.services.tests import models, schemas

def get_test_summary(db: Session, test_summary_id: int):
    return db.query(models.TestSummary).filter(models.TestSummary.id == test_summary_id).first()

def get_test_summary_by_author_email(db: Session, email: str):
    return db.query(models.TestSummary).filter(models.TestSummary.corresponding_author_email == email).first()

def get_test_summaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TestSummary).offset(skip).limit(limit).all()

def create_test_summary(db: Session, test_summary: schemas.TestSummaryCreate):
    db.add(test_summary)
    db.commit()
    db.refresh(test_summary)
    return test_summary

def get_test_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TestRun).offset(skip).limit(limit).all()

def create_test_summary_test_run(db: Session, test_run: schemas.TestRunCreate, test_summary_id: int):
    db_test_run = models.TestRun(**test_run.model_dump(), test_summary_id=test_summary_id)
    db.add(db_test_run)
    db.commit()
    db.refresh(db_test_run)
    return db_test_run
