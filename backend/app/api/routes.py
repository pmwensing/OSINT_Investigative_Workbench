from fastapi import APIRouter
from app.api.investigations import router as investigations_router

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

router.include_router(investigations_router)
