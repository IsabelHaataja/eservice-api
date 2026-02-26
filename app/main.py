from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.version import router as version_router
from app.api.cases import router as cases_router
from app.db.session import engine
from app.db.models import Base

app = FastAPI(title="eService Workflow API", version="0.1.0")

app.include_router(health_router, prefix="/api")
app.include_router(version_router, prefix="/api")
app.include_router(cases_router, prefix="/api")

Base.metadata.create_all(bind=engine)