from fastapi import APIRouter
from app.api.investigations import router as investigations_router
from app.api.intelligence import router as intelligence_router
from app.api.jobs import router as jobs_router
from app.api.contradictions import router as contradictions_router
from app.api.timeline import router as timeline_router

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

router.include_router(investigations_router)
router.include_router(intelligence_router)
router.include_router(jobs_router)
router.include_router(contradictions_router)
router.include_router(timeline_router)
