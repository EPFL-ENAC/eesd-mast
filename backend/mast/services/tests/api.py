from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from mast.services.tests import service, schemas
from mast.database import get_db

router = APIRouter()

@router.post("/test_summaries",
             status_code=200,
             description="-- Test summaries --"
             )
def create_test_summary(test_summary: schemas.TestSummaryCreate, db: Session = Depends(get_db)):
    return service.create_test_summary(db=db, test_summary=test_summary)

@router.get("/test_summaries/", response_model=list[schemas.TestSummary])
def read_test_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_summaries = service.get_test_summaries(db, skip=skip, limit=limit)
    return test_summaries

@router.get("/test_summaries/{test_summary_id}", response_model=schemas.TestSummary)
def read_test_summary(test_summary_id: int, db: Session = Depends(get_db)):
    db_test_summary = service.get_test_summary(db, test_summary_id=test_summary_id)
    if db_test_summary is None:
        raise HTTPException(status_code=404, detail="Test summary not found")
    return db_test_summary

@router.post("/test_summaries/{test_summary_id}/test_runs/", response_model=schemas.TestRun)
def create_test_run_for_test_summary(
    test_summary_id: int, test_run: schemas.TestRunCreate, db: Session = Depends(get_db)
):
    return service.create_test_summary_test_run(db=db, test_run=test_run, test_summary_id=test_summary_id)

@router.get("/test_runs/", response_model=list[schemas.TestRun])
def read_test_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_runs = service.get_test_runs(db, skip=skip, limit=limit)
    return test_runs