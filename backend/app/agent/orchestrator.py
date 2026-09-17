"""Master Conversation Orchestrator.

Implements the end-to-end processing pipeline:
Session Context -> Intent/Entity Extraction -> Deterministic Policy Engine ->
Action Execution -> Escalation Engine -> Grounded Response -> Audit Logging.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.models.customer import Customer
from app.models.booking import Booking
from app.models.policy import PolicyDecision, EscalationDecision
from app.models.action import ActionRecord
from app.models.audit import AuditEvent

from app.services.customer_service import customer_service
from app.services.booking_service import booking_service
from app.services.audit_service import audit_service

from app.agent.session import session_manager, SessionState
from app.agent.intent import IntentExtractor, ExtractionResult
from app.agent.policy_engine import PolicyEngine
from app.agent.escalation import EscalationEngine
from app.agent.action_engine import ActionEngine
from app.agent.response import ResponseGenerator


class ResolutionResponse(BaseModel):
    session_id: str
    customer_id: str
    customer_name: str
    pnr: str
    agent_message: str
    detected_intents: List[str]
    detected_sentiment: str
    policy_decisions: List[PolicyDecision]
    actions_taken: List[ActionRecord]
    escalated: bool
    escalation_reason: Optional[str] = None
    policy_citations: List[str]
    audit_event_id: str


class AgentOrchestrator:
    """Coordinates context resolution, intent parsing, deterministic policy checks, and simulated actions."""

    @classmethod
    def process_message(
        cls,
        user_message: str,
        session_id: Optional[str] = None,
        override_customer_id: Optional[str] = None
    ) -> ResolutionResponse:
        session = session_manager.get_or_create(session_id)

        # 1. Intent and Entity Extraction
        extraction: ExtractionResult = IntentExtractor.extract(user_message)
        intents = extraction.intents
        entities = extraction.entities
        sentiment = extraction.sentiment

        # 2. Customer and Booking Resolution
        customer = None
        booking = None

        # Prioritize explicit customer switch if provided from UI selector
        if override_customer_id:
            customer = customer_service.get_by_id(override_customer_id)
            if customer:
                booking = booking_service.get_by_pnr(customer.booking_reference)

        # Fallback to session context
        if not customer and session.customer_id:
            customer = customer_service.get_by_id(session.customer_id)
            if customer:
                booking = booking_service.get_by_pnr(customer.booking_reference)

        # Fallback to extracted entities
        if not customer:
            if "customer_name" in entities:
                customer = customer_service.get_by_name(entities["customer_name"])
            elif "pnr" in entities:
                customer = customer_service.get_by_pnr(entities["pnr"])

            if customer:
                booking = booking_service.get_by_pnr(customer.booking_reference)

        # Fallback default: Priya Nair (Demo starter)
        if not customer:
            customer = customer_service.get_by_id("CUST-001")
            booking = booking_service.get_by_pnr("SK4821X")

        assert customer is not None
        assert booking is not None

        # Update session
        session.customer_id = customer.customer_id
        session.customer_name = customer.name
        session.pnr = booking.booking_reference
        session.flight_number = booking.flight_number

        # 3. Privacy Boundary Check (Detect cross-customer inquiries)
        privacy_violation = False
        extracted_pnr = entities.get("pnr")
        if extracted_pnr and extracted_pnr.upper() != booking.booking_reference.upper():
            privacy_violation = True

        policy_decisions: List[PolicyDecision] = []
        actions_taken: List[ActionRecord] = []
        citations: List[str] = []

        if privacy_violation:
            escalation = EscalationDecision(
                escalate=False,
                triggers=["PRIVACY_CROSS_CUSTOMER_ATTEMPT"],
                reason="Inquiry about third-party booking reference rejected.",
                policy_sources=["Customer Privacy and Data Protection Standard"]
            )
            citations.append("Customer Privacy and Data Protection Standard")
        else:
            # 4. Deterministic Policy Evaluation

            # Cancellation & Refund / Rebooking evaluation
            if booking.status.lower() == "cancelled":
                chosen = None
                if "REFUND_REQUEST" in intents or entities.get("wants_cash"):
                    chosen = "REFUND"
                elif "REBOOKING_REQUEST" in intents:
                    chosen = "REBOOK"

                canc_decision = PolicyEngine.evaluate_cancellation(booking, chosen)
                policy_decisions.append(canc_decision)
                citations.extend(canc_decision.policy_sources)

                # Return flight evaluation (Priya Nair)
                ret_decision = PolicyEngine.evaluate_return_flight(booking)
                if ret_decision:
                    policy_decisions.append(ret_decision)
                    citations.extend(ret_decision.policy_sources)

            # Delay compensation evaluation
            if booking.status.lower() == "delayed":
                delay_decision = PolicyEngine.evaluate_delay_compensation(booking)
                policy_decisions.append(delay_decision)
                citations.extend(delay_decision.policy_sources)

            # Fare difference evaluation
            fare_diff = entities.get("fare_difference_inr")
            if fare_diff is not None or "FARE_DIFFERENCE_REQUEST" in intents:
                val = float(fare_diff) if fare_diff is not None else 2000.0
                fare_decision = PolicyEngine.evaluate_fare_difference(val)
                policy_decisions.append(fare_decision)
                citations.extend(fare_decision.policy_sources)

            # Loyalty tier evaluation
            upgrade_requested = (
                "UPGRADE_REQUEST" in intents
                or entities.get("requests_cabin_upgrade", False)
                or entities.get("requested_monetary_compensation_inr", 0) > 0
            )
            loyalty_decision = PolicyEngine.evaluate_loyalty(customer.loyalty_tier, upgrade_requested)
            if loyalty_decision:
                policy_decisions.append(loyalty_decision)
                citations.extend(loyalty_decision.policy_sources)

            # 5. Escalation Evaluation
            escalation = EscalationEngine.evaluate(
                user_message=user_message,
                detected_intents=intents,
                extracted_entities=entities,
                policy_decisions=policy_decisions
            )
            if escalation.escalate:
                citations.extend(escalation.policy_sources)

            # 6. Action Execution (Simulated)
            # Execute Refund
            if (
                booking.status.lower() == "cancelled"
                and ("REFUND_REQUEST" in intents or entities.get("wants_cash"))
                and not any(a.action_type == "REFUND_REQUESTED" for a in session.executed_actions)
            ):
                act = ActionEngine.initiate_refund(customer, booking)
                actions_taken.append(act)
                session.executed_actions.append(act)

            # Execute Rebooking
            if (
                booking.status.lower() == "cancelled"
                and "REBOOKING_REQUEST" in intents
                and not any(a.action_type == "REBOOKING_REQUESTED" for a in session.executed_actions)
            ):
                act = ActionEngine.request_rebooking(customer, booking)
                actions_taken.append(act)
                session.executed_actions.append(act)

            # Execute Delay compensations
            if booking.status.lower() == "delayed":
                # Meal voucher
                if not any(a.action_type == "MEAL_VOUCHER_ISSUED" for a in session.executed_actions):
                    val = 500 if booking.delay_hours < 3.0 else None
                    act = ActionEngine.issue_meal_voucher(customer, booking, val)
                    actions_taken.append(act)
                    session.executed_actions.append(act)

                # Lounge access if > 3h
                if booking.delay_hours > 3.0 and not any(a.action_type == "LOUNGE_ACCESS_ISSUED" for a in session.executed_actions):
                    act = ActionEngine.issue_lounge_access(customer, booking)
                    actions_taken.append(act)
                    session.executed_actions.append(act)

                # Hotel if > 5h
                if (
                    booking.delay_hours > 5.0
                    and ("HOTEL_REQUEST" in intents or "wants_full_night_hotel" in entities or booking.delay_hours >= 6.0)
                    and not any(a.action_type == "HOTEL_REQUESTED_FOR_DELAYED_HOURS" for a in session.executed_actions)
                ):
                    act = ActionEngine.arrange_hotel(customer, booking)
                    actions_taken.append(act)
                    session.executed_actions.append(act)

            # Execute Escalation ticket if triggered
            if escalation.escalate and not session.escalated:
                act = ActionEngine.create_escalation_ticket(
                    customer,
                    booking,
                    escalation.triggers,
                    escalation.reason or "Escalation requested"
                )
                actions_taken.append(act)
                session.executed_actions.append(act)
                session.escalated = True
                session.escalation_ticket_id = act.details.get("ticket_id")

        # 7. Generate Grounded Response
        agent_message = ResponseGenerator.generate(
            customer=customer,
            booking=booking,
            sentiment=sentiment,
            policy_decisions=policy_decisions,
            actions_taken=actions_taken,
            escalation=escalation,
            unaffected_return_noted=(booking.return_flight is not None),
            privacy_violation_attempt=privacy_violation
        )

        # 8. Record Audit Event
        audit_id = f"AUD-{uuid.uuid4().hex[:8].upper()}"
        clean_citations = sorted(list(set(citations)))
        audit_event = AuditEvent(
            audit_id=audit_id,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=session.session_id,
            customer_id=customer.customer_id,
            customer_name=customer.name,
            pnr=booking.booking_reference,
            user_message=user_message,
            detected_intents=intents,
            detected_sentiment=sentiment,
            extracted_entities=entities,
            policy_decisions=policy_decisions,
            actions_taken=actions_taken,
            escalated=escalation.escalate,
            escalation_reason=escalation.reason,
            policy_citations=clean_citations,
            agent_response=agent_message
        )
        audit_service.record_event(audit_event)

        # Update session history
        session.history.append({"role": "user", "content": user_message})
        session.history.append({"role": "agent", "content": agent_message})
        session_manager.update_session(session)

        return ResolutionResponse(
            session_id=session.session_id,
            customer_id=customer.customer_id,
            customer_name=customer.name,
            pnr=booking.booking_reference,
            agent_message=agent_message,
            detected_intents=intents,
            detected_sentiment=sentiment,
            policy_decisions=policy_decisions,
            actions_taken=actions_taken,
            escalated=escalation.escalate,
            escalation_reason=escalation.reason,
            policy_citations=clean_citations,
            audit_event_id=audit_id
        )
