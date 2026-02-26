from sqlalchemy.orm import Session
from app.db.models import Case

class CaseServiceDB:
    def create(self, db: Session, title: str):
        case = Case(title=title, status="submitted")
        db.add(case)
        db.commit()
        db.refresh(case)
        return {
            "id": case.id,
            "title": case.title,
            "status": case.status,
            "created_at": case.created_at.isoformat(),
        }

    def list(self, db: Session):
        cases = db.query(Case).order_by(Case.id.desc()).all()
        return [{
            "id": c.id,
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at.isoformat(),
        } for c in cases]

    def get(self, db: Session, case_id: int):
        c = db.get(Case, case_id)
        if not c:
            return None
        return {
            "id": c.id,
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at.isoformat(),
        }

    def update_status(self, db: Session, case_id: int, status: str):
        c = db.get(Case, case_id)
        if not c:
            return None
        c.status = status
        db.commit()
        db.refresh(c)
        return {
            "id": c.id,
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at.isoformat(),
        }

case_service_db = CaseServiceDB()