from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.graph_engine import (
    build_graph_payload,
    get_neighbors,
    shortest_path,
    degree_centrality,
    connected_components,
    neo4j_projection_payload,
)

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

@router.get("/centrality")
def centrality(investigation_id: str, db: Session = Depends(get_db)):
    return degree_centrality(db, investigation_id)

@router.get("/clusters")
def clusters(investigation_id: str, db: Session = Depends(get_db)):
    return connected_components(db, investigation_id)

@router.get("/neo4j_export")
def neo4j_export(investigation_id: str, db: Session = Depends(get_db)):
    return neo4j_projection_payload(db, investigation_id)
