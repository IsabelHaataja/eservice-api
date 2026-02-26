from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["meta"])

@router.get("/version")
def version():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }