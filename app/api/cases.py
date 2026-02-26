from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.case_service import case_service
from enum import Enum

router = APIRouter(tags=["cases"])

class CaseStatus(str, Enum):
    submitted = "submitted"
    processing = "processing"
    done = "done"
    rejected = "rejected"

class CaseOut(BaseModel):
    id: int
    title: str
    status: CaseStatus
    created_at: str

class CaseCreate(BaseModel):
    title: str

class CaseUpdateStatus(BaseModel):
    status: CaseStatus


@router.post("/cases", response_model=CaseOut)
def create_case(payload: CaseCreate):
    return case_service.create(payload.title)


@router.get("/cases", response_model=list[CaseOut])
def list_cases():
    return case_service.list()


@router.get("/cases/{case_id}", response_model=CaseOut)
def get_case(case_id: int):
    case = case_service.get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.patch("/cases/{case_id}/status", response_model=CaseOut)
def update_case_status(case_id: int, payload: CaseUpdateStatus):
    case = case_service.update_status(case_id, payload.status)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case