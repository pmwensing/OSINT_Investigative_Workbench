from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import settings
from api.routes import auth, investigations, targets, jobs, graph, timeline, artifacts

app = FastAPI(title="OSINT Workbench API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": "OSINT Workbench API", "env": "production-like"}

app.include_router(auth.router, prefix="/api/v1")
app.include_router(investigations.router, prefix="/api/v1")
app.include_router(targets.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(graph.router, prefix="/api/v1")
app.include_router(timeline.router, prefix="/api/v1")
app.include_router(artifacts.router, prefix="/api/v1")
