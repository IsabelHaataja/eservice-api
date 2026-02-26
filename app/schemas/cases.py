from pydantic import BaseModel
from enum import Enum

class CaseStatus(str, Enum):
    submitted = "submitted"
    processing = "processing"
    done = "done"
    rejected = "rejected"

class CaseCreate(BaseModel):
    title: str

class CaseUpdateStatus(BaseModel):
    status: CaseStatus

class CaseOut(BaseModel):
    id: int
    title: str
    status: CaseStatus
    created_at: str