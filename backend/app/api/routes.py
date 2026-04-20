from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/investigations")
def list_investigations():
    return []
