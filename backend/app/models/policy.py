from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PolicyRule(BaseModel):
    policy_id: str
    section: str
    name: str
    description: str
    allowed_actions: List[str] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)
    citation: str


class PolicyDecision(BaseModel):
    eligible: bool
    policy_id: str
    policy_name: str
    allowed_actions: List[str] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)
    escalation_required: bool = False
    escalation_reason: Optional[str] = None
    policy_sources: List[str] = Field(default_factory=list)
    explanation: str
    details: Dict[str, Any] = Field(default_factory=dict)


class EscalationDecision(BaseModel):
    escalate: bool
    triggers: List[str] = Field(default_factory=list)
    reason: Optional[str] = None
    policy_sources: List[str] = Field(default_factory=list)
    recommended_action: str = "CONTINUE"
