from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ActionRecord(BaseModel):
    action_id: str
    action_type: str
    customer_id: str
    booking_reference: str
    status: str
    timestamp: str
    policy_reference: str
    reason: str
    details: Dict[str, Any] = Field(default_factory=dict)
    is_simulated: bool = True
    disclaimer: str = "SIMULATED DEMO ACTION — No live external airline GDS/payment system modified."
