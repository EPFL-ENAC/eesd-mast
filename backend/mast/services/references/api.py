from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from mast.services.references import service, schemas
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
