from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["meta"])

@router.get("/version")
def version():
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }