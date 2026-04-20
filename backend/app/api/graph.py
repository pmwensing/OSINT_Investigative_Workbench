from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.graph_engine import build_graph_payload, get_neighbors, shortest_path

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/")
def get_graph(investigation_id: str, db: Session = Depends(get_db)):
    return build_graph_payload(db, investigation_id)

@router.get("/neighbors")
def neighbors(investigation_id: str, entity_id: str, db: Session = Depends(get_db)):
    return get_neighbors(db, investigation_id, entity_id)

@router.get("/path")
def path(investigation_id: str, source_id: str, target_id: str, db: Session = Depends(get_db)):
    return shortest_path(db, investigation_id, source_id, target_id)
