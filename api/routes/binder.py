from fastapi import APIRouter

router = APIRouter(tags=["binder"])

@router.get("/binder/health")
def binder_health():
    return {"status": "ok"}
