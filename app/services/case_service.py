from datetime import datetime, timezone
from typing import Dict, List, Optional


class CaseService:
    def __init__(self):
        self._cases: Dict[int, dict] = {}
        self._next_id = 1

    def create(self, title: str) -> dict:
        case_id = self._next_id
        self._next_id += 1

        case = {
            "id": case_id,
            "title": title,
            "status": "submitted",
            "created_at": datetime.now(timezone.utc).isoformat() + "Z",
        }
        self._cases[case_id] = case
        return case

    def list(self) -> List[dict]:
        return list(self._cases.values())

    def get(self, case_id: int) -> Optional[dict]:
        return self._cases.get(case_id)

    def update_status(self, case_id: int, status: str) -> Optional[dict]:
        case = self._cases.get(case_id)
        if not case:
            return None
        case["status"] = status
        return case


case_service = CaseService()