"""Escalation Engine for Airline Customer Resolution Agent.

Implements strict Section 7.0 Prohibited Actions & Mandatory Escalation Rules.
Ensures the agent never oversteps authority or dismisses mandatory escalation triggers.
"""

import re
from typing import List, Dict, Any, Optional
from app.models.policy import EscalationDecision
from app.config import AGENT_WAIVER_LIMIT_INR


class EscalationEngine:
    """Evaluates customer input and context against mandatory escalation triggers."""

    LEGAL_PATTERNS = [
        r"\blegal\s+action\b",
        r"\blawyer\b",
        r"\bsue\b",
        r"\bcourt\b",
        r"\blitigat(e|ion)\b",
        r"\bconsumer\s+forum\b",
        r"\bconsumer\s+court\b",
        r"\blegal\s+notice\b"
    ]

    FORMAL_COMPLAINT_PATTERNS = [
        r"\bformal\s+complaint\b",
        r"\bofficial\s+complaint\b",
        r"\bdgca\b",
        r"\baviation\s+ministry\b",
        r"\bgrievance\s+officer\b",
        r"\bescalat(e|ion)\s+to\s+regulator\b"
    ]

    DIFFERENT_PAYMENT_PATTERNS = [
        r"\bdifferent\s+(card|account|payment|method|bank)\b",
        r"\banother\s+(card|account|payment|method|bank)\b",
        r"\bcash\s+(refund|payout|compensation)\b",
        r"\btransfer\s+to\s+(upi|paytm|googlepay|phonepe)\b",
        r"\brefund\s+to\s+(cash|another|different)\b"
    ]

    @classmethod
    def evaluate(
        cls,
        user_message: str,
        detected_intents: List[str],
        extracted_entities: Dict[str, Any],
        policy_decisions: Optional[List[Any]] = None
    ) -> EscalationDecision:
        triggers: List[str] = []
        reasons: List[str] = []
        sources = ["Service Rules Section 7.0: Prohibited Actions"]

        msg_lower = user_message.lower()

        # 1. Check legal action threats
        for pat in cls.LEGAL_PATTERNS:
            if re.search(pat, msg_lower):
                triggers.append("LEGAL_ACTION_THREAT")
                reasons.append("Customer threatened legal action or litigation.")
                break

        # 2. Check formal complaint threats
        for pat in cls.FORMAL_COMPLAINT_PATTERNS:
            if re.search(pat, msg_lower):
                triggers.append("FORMAL_COMPLAINT_THREAT")
                reasons.append("Customer threatened to lodge a formal regulatory/official complaint.")
                break

        # 3. Check different payment method or cash refund requests
        for pat in cls.DIFFERENT_PAYMENT_PATTERNS:
            if re.search(pat, msg_lower):
                triggers.append("DIFFERENT_PAYMENT_METHOD_REQUEST")
                reasons.append("Customer requested refund to a different payment method or cash payout.")
                break

        # 4. Check fare difference waiver requests exceeding limit
        fare_diff = extracted_entities.get("fare_difference_inr")
        if fare_diff is not None and float(fare_diff) > AGENT_WAIVER_LIMIT_INR:
            triggers.append("FARE_DIFF_WAIVER_EXCEEDS_1500")
            reasons.append(
                f"Requested fare difference waiver of ₹{fare_diff:,.0f} exceeds the agent limit of ₹{AGENT_WAIVER_LIMIT_INR:,.0f}."
            )
            sources.append("Service Rules Section 5.4: Fare Difference Rule")

        # 5. Check out-of-policy compensation / free cabin upgrade
        if "UPGRADE_REQUEST" in detected_intents or extracted_entities.get("requests_cabin_upgrade"):
            triggers.append("COMPENSATION_EXCEEDS_POLICY")
            reasons.append("Customer requested complimentary cabin upgrade/extra compensation not provided in disruption policy.")
            sources.append("Service Rules Section 5.5: Loyalty Tier Rule")

        if extracted_entities.get("requested_monetary_compensation_inr", 0) > 0:
            triggers.append("COMPENSATION_EXCEEDS_POLICY")
            reasons.append("Customer requested arbitrary monetary compensation outside disruption policy.")

        # 6. Check policy decisions for downstream escalations
        if policy_decisions:
            for decision in policy_decisions:
                if getattr(decision, "escalation_required", False):
                    reason = getattr(decision, "escalation_reason", "Policy threshold exceeded.")
                    if reason not in triggers:
                        triggers.append(reason)
                        reasons.append(getattr(decision, "explanation", reason))

        if triggers:
            return EscalationDecision(
                escalate=True,
                triggers=list(set(triggers)),
                reason=" | ".join(reasons),
                policy_sources=list(set(sources)),
                recommended_action="ESCALATE_TO_HUMAN_SUPERVISOR"
            )

        return EscalationDecision(
            escalate=False,
            triggers=[],
            reason=None,
            policy_sources=sources,
            recommended_action="CONTINUE_AGENT_RESOLUTION"
        )
