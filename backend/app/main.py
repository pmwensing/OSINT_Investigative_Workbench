from fastapi import FastAPI
from app.api.routes import router
from app.db.session import Base, engine
from app.models import investigation, target, entity

app = FastAPI(title="OSINT Workbench API", version="v1")

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok", "app": "OSINT Workbench API"}
