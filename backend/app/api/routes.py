from fastapi import APIRouter
from app.api.investigations import router as investigations_router
from app.api.intelligence import router as intelligence_router
from app.api.jobs import router as jobs_router
from app.api.contradictions import router as contradictions_router
from app.api.timeline import router as timeline_router
from app.api.credibility import router as credibility_router
from app.api.graph import router as graph_router
from app.api.provenance import router as provenance_router
from app.api.decision import router as decision_router
from app.api.review import router as review_router
from app.api.report import router as report_router
from app.api.narrative import router as narrative_router

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

router.include_router(investigations_router)
router.include_router(intelligence_router)
router.include_router(jobs_router)
router.include_router(contradictions_router)
router.include_router(timeline_router)
router.include_router(credibility_router)
router.include_router(graph_router)
router.include_router(provenance_router)
router.include_router(decision_router)
router.include_router(review_router)
router.include_router(report_router)
router.include_router(narrative_router)
