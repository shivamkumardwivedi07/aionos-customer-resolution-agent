import json
from typing import List, Optional
from app.models.audit import AuditEvent


class AuditService:
    def __init__(self):
        self._events: List[AuditEvent] = []

    def record_event(self, event: AuditEvent) -> AuditEvent:
        self._events.append(event)
        return event

    def get_all(self) -> List[AuditEvent]:
        return list(reversed(self._events))

    def get_by_session(self, session_id: str) -> List[AuditEvent]:
        return [e for e in self._events if e.session_id == session_id]

    def get_by_pnr(self, pnr: str) -> List[AuditEvent]:
        clean_pnr = pnr.strip().upper()
        return [e for e in self._events if e.pnr.upper() == clean_pnr]

    def clear(self) -> None:
        self._events.clear()

    def export_json(self) -> str:
        return json.dumps([e.model_dump() for e in self._events], indent=2)


audit_service = AuditService()
