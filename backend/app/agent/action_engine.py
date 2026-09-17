"""Simulated Action Execution Engine.

Executes permitted airline operations actions in simulated demo mode.
Clearly tags all actions with simulation markers and audit identifiers.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models.action import ActionRecord
from app.models.booking import Booking
from app.models.customer import Customer


class ActionEngine:
    """Executes permitted simulated actions grounded in policy decisions."""

    @staticmethod
    def _generate_action_id(prefix: str) -> str:
        return f"SIM-{prefix}-{uuid.uuid4().hex[:6].upper()}"

    @classmethod
    def initiate_refund(cls, customer: Customer, booking: Booking) -> ActionRecord:
        action_id = cls._generate_action_id("REF")
        return ActionRecord(
            action_id=action_id,
            action_type="REFUND_REQUESTED",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="SUBMITTED_TO_PAYMENT_PROCESSOR",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 5.1 & 5.3",
            reason=f"Full refund requested for cancelled flight {booking.flight_number}",
            details={
                "refund_method": "ORIGINAL_PAYMENT_METHOD_ONLY",
                "sla_window": "7 business days",
                "estimated_completion": "By Wednesday, 30 September 2026",
                "amount": "Full Fare (100%)"
            }
        )

    @classmethod
    def issue_meal_voucher(cls, customer: Customer, booking: Booking, amount_inr: Optional[int] = None) -> ActionRecord:
        action_id = cls._generate_action_id("VOUCH")
        val_str = f"₹{amount_inr}" if amount_inr else "Full Airport Meal Allowance"
        return ActionRecord(
            action_id=action_id,
            action_type="MEAL_VOUCHER_ISSUED",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="ISSUED_DIGITALLY",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 5.2",
            reason=f"Disruption meal voucher for {booking.delay_hours:.1f}h delay on {booking.flight_number}",
            details={
                "voucher_code": f"MEAL-{uuid.uuid4().hex[:4].upper()}",
                "value": val_str,
                "valid_airports": [booking.route.split("→")[0].strip()]
            }
        )

    @classmethod
    def issue_lounge_access(cls, customer: Customer, booking: Booking) -> ActionRecord:
        action_id = cls._generate_action_id("LNG")
        origin = booking.route.split("→")[0].strip()
        return ActionRecord(
            action_id=action_id,
            action_type="LOUNGE_ACCESS_ISSUED",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="ACTIVATED",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 5.2",
            reason=f"Complimentary lounge access for {booking.delay_hours:.1f}h delay (> 3h threshold)",
            details={
                "lounge_pass_code": f"LOUNGE-PASS-{uuid.uuid4().hex[:4].upper()}",
                "valid_airport": origin,
                "valid_until": booking.current_departure or "Departure"
            }
        )

    @classmethod
    def arrange_hotel(cls, customer: Customer, booking: Booking) -> ActionRecord:
        action_id = cls._generate_action_id("HTL")
        return ActionRecord(
            action_id=action_id,
            action_type="HOTEL_REQUESTED_FOR_DELAYED_HOURS",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="REQUESTED_TRANSIT_DAY_ROOM",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 5.2",
            reason=f"Day-use transit hotel accommodation covering {booking.delay_hours:.1f} delayed hours",
            details={
                "hotel_booking_ref": f"HTL-{uuid.uuid4().hex[:5].upper()}",
                "coverage_scope": f"Delayed hours window ({booking.original_departure} to {booking.current_departure})",
                "restriction": "Transit room only — full night's stay is NOT eligible"
            }
        )

    @classmethod
    def request_rebooking(cls, customer: Customer, booking: Booking) -> ActionRecord:
        action_id = cls._generate_action_id("REBK")
        priority = "PRIORITY_STANDBY" if customer.loyalty_tier in ["Gold", "Platinum"] else "STANDARD"
        return ActionRecord(
            action_id=action_id,
            action_type="REBOOKING_REQUESTED",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="PENDING_AIRPORT_ASSIGNMENT",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 5.1 & 5.5",
            reason=f"Free 24h rebooking request initiated for cancelled {booking.flight_number}",
            details={
                "priority_queue": priority,
                "rebooking_window": "Next available flight within 24 hours",
                "fare_charged": 0.0,
                "disclaimer": "Ground operations will confirm physical seat assignment upon check-in"
            }
        )

    @classmethod
    def create_escalation_ticket(
        cls,
        customer: Customer,
        booking: Booking,
        triggers: List[str],
        reason: str
    ) -> ActionRecord:
        action_id = cls._generate_action_id("ESC")
        return ActionRecord(
            action_id=action_id,
            action_type="ESCALATED_TO_HUMAN",
            customer_id=customer.customer_id,
            booking_reference=booking.booking_reference,
            status="ESCALATED_TO_SUPERVISOR_QUEUE",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            policy_reference="Service Rules Section 7.0: Prohibited Actions",
            reason=reason,
            details={
                "ticket_id": f"ESC-TCK-{uuid.uuid4().hex[:6].upper()}",
                "triggers": triggers,
                "priority": "HIGH" if "LEGAL_ACTION_THREAT" in triggers else "STANDARD",
                "assigned_department": "Customer Relations & Legal Supervision"
            }
        )
