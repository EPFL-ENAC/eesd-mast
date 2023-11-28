from sqlalchemy.orm import Session
from mast.services.references import models

def get_references(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reference).offset(skip).limit(limit).all()

def get_reference(db: Session, reference_id: int):
    return db.query(models.Reference).filter(models.Reference.id == reference_id).first()
