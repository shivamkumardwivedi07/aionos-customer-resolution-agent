"""Conversation and Session State Management.

Preserves active customer identity, PNR, flight status, pending choices,
and action history across multi-turn interactions.
"""

import uuid
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from app.models.action import ActionRecord


class SessionState(BaseModel):
    session_id: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    pnr: Optional[str] = None
    flight_number: Optional[str] = None
    pending_choice: Optional[str] = None  # e.g. "AWAITING_CANCELLATION_SELECTION"
    executed_actions: List[ActionRecord] = Field(default_factory=list)
    escalated: bool = False
    escalation_ticket_id: Optional[str] = None
    history: List[Dict[str, str]] = Field(default_factory=list)


class SessionManager:
    """In-memory session registry with contextual multi-turn resolution."""

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> SessionState:
        if not session_id:
            session_id = str(uuid.uuid4())

        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)

        return self._sessions[session_id]

    def update_session(self, state: SessionState) -> None:
        self._sessions[state.session_id] = state

    def reset_session(self, session_id: str) -> SessionState:
        new_state = SessionState(session_id=session_id)
        self._sessions[session_id] = new_state
        return new_state

    def clear_all(self) -> None:
        self._sessions.clear()


session_manager = SessionManager()
