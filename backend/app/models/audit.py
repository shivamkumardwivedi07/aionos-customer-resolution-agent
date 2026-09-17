from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.policy import PolicyDecision
from app.models.action import ActionRecord


class AuditEvent(BaseModel):
    audit_id: str
    timestamp: str
    session_id: str
    customer_id: str
    customer_name: str
    pnr: str
    user_message: str
    detected_intents: List[str] = Field(default_factory=list)
    detected_sentiment: str = "Neutral"
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    policy_decisions: List[PolicyDecision] = Field(default_factory=list)
    actions_taken: List[ActionRecord] = Field(default_factory=list)
    escalated: bool = False
    escalation_reason: Optional[str] = None
    policy_citations: List[str] = Field(default_factory=list)
    agent_response: str
