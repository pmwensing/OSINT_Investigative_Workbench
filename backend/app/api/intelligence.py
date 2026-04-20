from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.target import Target
from app.models.entity import Entity, Claim, Artifact, Relationship
from app.schemas.common import (
    TargetCreate, TargetRead,
    EntityCreate, EntityRead,
    ClaimCreate, ClaimRead,
    ArtifactCreate, ArtifactRead,
    RelationshipCreate, RelationshipRead
)

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

# TARGETS
@router.post("/targets", response_model=TargetRead)
def create_target(data: TargetCreate, db: Session = Depends(get_db)):
    obj = Target(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/targets", response_model=list[TargetRead])
def list_targets(db: Session = Depends(get_db)):
    return db.query(Target).all()

# ENTITIES
@router.post("/entities", response_model=EntityRead)
def create_entity(data: EntityCreate, db: Session = Depends(get_db)):
    obj = Entity(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/entities", response_model=list[EntityRead])
def list_entities(db: Session = Depends(get_db)):
    return db.query(Entity).all()

# CLAIMS
@router.post("/claims", response_model=ClaimRead)
def create_claim(data: ClaimCreate, db: Session = Depends(get_db)):
    obj = Claim(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/claims", response_model=list[ClaimRead])
def list_claims(db: Session = Depends(get_db)):
    return db.query(Claim).all()

# ARTIFACTS
@router.post("/artifacts", response_model=ArtifactRead)
def create_artifact(data: ArtifactCreate, db: Session = Depends(get_db)):
    obj = Artifact(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/artifacts", response_model=list[ArtifactRead])
def list_artifacts(db: Session = Depends(get_db)):
    return db.query(Artifact).all()

# RELATIONSHIPS
@router.post("/relationships", response_model=RelationshipRead)
def create_relationship(data: RelationshipCreate, db: Session = Depends(get_db)):
    obj = Relationship(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/relationships", response_model=list[RelationshipRead])
def list_relationships(db: Session = Depends(get_db)):
    return db.query(Relationship).all()
