from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.provenance_engine import create_provenance, cite_claim

router = APIRouter(prefix="/provenance", tags=["provenance"])

@router.post("/record")
def create_record(investigation_id: str, content: str, db: Session = Depends(get_db)):
    record = create_provenance(db, investigation_id, content=content)
    return {"id": str(record.id), "hash": record.content_hash}

@router.post("/cite")
def cite(claim_id: str, excerpt: str, db: Session = Depends(get_db)):
    citation = cite_claim(db, claim_id, excerpt=excerpt)
    return {"id": str(citation.id)}
