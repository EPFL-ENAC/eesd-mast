from sqlalchemy.orm import Session
from mast.services.references import models, schemas
from mast.services.experiments import service as experiments_service

def get_references(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reference).offset(skip).limit(limit).all()

def get_reference(db: Session, reference_id: int):
    return db.query(models.Reference).filter(models.Reference.id == reference_id).first()

def create_reference(db: Session, reference: schemas.ReferenceCreate):
    db.add(reference)
    db.commit()
    db.refresh(reference)
    return reference

def delete_reference(db: Session, reference_id: int):
    experiments_service.delete_reference_experiments(db, reference_id)
    db.query(models.Reference).filter(models.Reference.id == reference_id).delete()
    db.commit()