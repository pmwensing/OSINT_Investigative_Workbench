from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="OSINT Workbench API", version="v1")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok", "app": "OSINT Workbench API"}
