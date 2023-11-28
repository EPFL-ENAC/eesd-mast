from fastapi import Depends, Security, APIRouter, HTTPException
from sqlalchemy.orm import Session

from mast.services.references import service, schemas, models
from mast.database import get_db
from mast.auth import get_api_key

router = APIRouter()

@router.get("/references/", response_model=list[schemas.Reference])
def read_references(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    refs = service.get_references(db, skip=skip, limit=limit)
    return refs

@router.post("/references",
             status_code=200,
             description="-- References --"
             )
def create_reference(reference: schemas.ReferenceCreate, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    db_ref = models.Reference(**reference.dict())
    return service.create_reference(db=db, reference=db_ref)

@router.get("/references/{reference_id}", response_model=schemas.Reference)
def read_reference(reference_id: int, db: Session = Depends(get_db)):
    db_ref = service.get_reference(db, reference_id=reference_id)
    if db_ref is None:
        raise HTTPException(status_code=404, detail="Reference not found")
    return db_ref

@router.delete("/references/{reference_id}")
def read_reference(reference_id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    service.delete_reference(db, reference_id=reference_id)
