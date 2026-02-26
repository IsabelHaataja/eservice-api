from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.case_service_db import case_service_db
from app.schemas.cases import CaseCreate, CaseUpdateStatus, CaseOut

router = APIRouter(tags=["cases"])

@router.post("/cases", response_model=CaseOut)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    return case_service_db.create(db, payload.title)


@router.get("/cases", response_model=list[CaseOut])
def list_cases(db: Session = Depends(get_db)):
    return case_service_db.list(db)


@router.get("/cases/{case_id}", response_model=CaseOut)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = case_service_db.get(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.patch("/cases/{case_id}/status", response_model=CaseOut)
def update_case_status(case_id: int, payload: CaseUpdateStatus, db: Session = Depends(get_db)):
    case = case_service_db.update_status(db, case_id, payload.status.value)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case