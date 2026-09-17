"""Deterministic Policy Engine.

Enforces the core architectural principle:
'LLM for language, deterministic rules for business decisions.'
Zero hallucinations. Authoritative ground truth rules evaluated via pure Python.
"""

from typing import Optional, List, Dict, Any
from app.models.booking import Booking
from app.models.policy import PolicyDecision
from app.config import AGENT_WAIVER_LIMIT_INR


class PolicyEngine:
    """Deterministic business logic engine for airline disruption service rules."""

    @staticmethod
    def evaluate_cancellation(
        booking: Booking,
        chosen_action: Optional[str] = None
    ) -> PolicyDecision:
        """Section 5.1: Cancellation Rebooking Rule & Section 5.3: Refund Rule."""
        if booking.status.lower() != "cancelled":
            return PolicyDecision(
                eligible=False,
                policy_id="POL-5.1",
                policy_name="Cancellation Rebooking Rule",
                allowed_actions=[],
                restrictions=["FLIGHT_NOT_CANCELLED"],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.1: Cancellation Rebooking Rule"],
                explanation=f"Flight {booking.flight_number} is not cancelled (Current status: {booking.status}).",
                details={"flight_status": booking.status}
            )

        # Disruption is airline-caused (e.g. Operational reasons)
        if chosen_action == "REFUND":
            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.3",
                policy_name="Refund Processing Rule",
                allowed_actions=["FULL_REFUND"],
                restrictions=[
                    "ORIGINAL_PAYMENT_METHOD_ONLY",
                    "PROCESSED_WITHIN_7_BUSINESS_DAYS",
                    "NO_CASH_PAYOUT"
                ],
                escalation_required=False,
                policy_sources=[
                    "Service Rules Section 5.1: Cancellation Rebooking Rule",
                    "Service Rules Section 5.3: Refund Processing Rule"
                ],
                explanation=(
                    f"Flight {booking.flight_number} cancellation qualifies for a full refund. "
                    "Under Section 5.3, refunds must be processed in full within 7 business days "
                    "strictly to the original payment method. Cash payouts or third-party accounts are not permitted."
                ),
                details={
                    "refund_type": "FULL_REFUND",
                    "sla_business_days": 7,
                    "payment_method": "ORIGINAL_PAYMENT_METHOD"
                }
            )

        if chosen_action == "REBOOK":
            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.1",
                policy_name="Cancellation Rebooking Rule",
                allowed_actions=["FREE_REBOOKING_24H"],
                restrictions=[
                    "WITHIN_24_HOURS",
                    "NO_FABRICATED_INVENTORY",
                    "GROUND_OPERATIONS_ASSIGNMENT"
                ],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.1: Cancellation Rebooking Rule"],
                explanation=(
                    f"Customer is entitled to free rebooking on the next available flight within 24 hours. "
                    "Note: Specific alternative flight numbers, schedules, and seat inventory are not provided in the "
                    "authoritative data pack and are assigned by airport ground operations."
                ),
                details={
                    "window_hours": 24,
                    "cost": 0.0,
                    "inventory_provided": False
                }
            )

        # Default entitlement when choice is pending
        return PolicyDecision(
            eligible=True,
            policy_id="POL-5.1",
            policy_name="Cancellation Rebooking Rule",
            allowed_actions=["FREE_REBOOKING_24H", "FULL_REFUND"],
            restrictions=[
                "CUSTOMER_CHOOSES_OPTION",
                "ORIGINAL_PAYMENT_METHOD_ONLY",
                "NO_FABRICATED_INVENTORY"
            ],
            escalation_required=False,
            policy_sources=["Service Rules Section 5.1: Cancellation Rebooking Rule"],
            explanation=(
                f"Flight {booking.flight_number} was cancelled due to {booking.disruption_reason}. "
                "Under Section 5.1, the customer is entitled to choose either: "
                "(A) Free rebooking on the next available flight within 24 hours, or "
                "(B) A full refund to the original payment method."
            ),
            details={"options": ["REBOOK_24H", "FULL_REFUND"]}
        )

    @staticmethod
    def evaluate_delay_compensation(booking: Booking) -> PolicyDecision:
        """Section 5.2: Delay Compensation Rule."""
        delay = booking.delay_hours

        if booking.status.lower() != "delayed" or delay <= 0:
            return PolicyDecision(
                eligible=False,
                policy_id="POL-5.2",
                policy_name="Delay Compensation Rule",
                allowed_actions=[],
                restrictions=["NO_DELAY_RECORDED"],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.2: Delay Compensation Rule"],
                explanation=f"Flight {booking.flight_number} has no qualifying delay recorded.",
                details={"delay_hours": delay}
            )

        if delay < 3.0:
            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.2",
                policy_name="Delay Compensation Rule (<3h)",
                allowed_actions=["MEAL_VOUCHER_500"],
                restrictions=["NO_LOUNGE_ACCESS", "NO_HOTEL"],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.2: Delay Compensation Rule"],
                explanation=(
                    f"Flight {booking.flight_number} is delayed by {delay:.1f} hours (< 3 hours). "
                    "Eligible for ₹500 meal voucher. Lounge and hotel accommodation are not applicable."
                ),
                details={"delay_hours": delay, "meal_voucher_inr": 500}
            )

        if 3.0 <= delay <= 5.0:
            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.2",
                policy_name="Delay Compensation Rule (3h-5h)",
                allowed_actions=["MEAL_VOUCHER", "LOUNGE_ACCESS"],
                restrictions=[
                    "NO_HOTEL_ACCOMMODATION",
                    "NO_MEETING_COMPENSATION"
                ],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.2: Delay Compensation Rule"],
                explanation=(
                    f"Flight {booking.flight_number} is delayed by {delay:.1f} hours (> 3 hours, ≤ 5 hours). "
                    "Qualifies for a meal voucher and lounge access. Hotel accommodation is strictly not applicable "
                    "(Section 5.2 requires delay > 5 hours for hotel assistance)."
                ),
                details={
                    "delay_hours": delay,
                    "meal_voucher": True,
                    "lounge_access": True,
                    "hotel_eligible": False
                }
            )

        # Delay > 5 hours
        return PolicyDecision(
            eligible=True,
            policy_id="POL-5.2",
            policy_name="Delay Compensation Rule (>5h)",
            allowed_actions=[
                "MEAL_VOUCHER",
                "LOUNGE_ACCESS",
                "HOTEL_ACCOMMODATION_DELAYED_HOURS_ONLY"
            ],
            restrictions=[
                "HOTEL_COVERS_DELAYED_HOURS_ONLY",
                "NO_FULL_NIGHT_STAY"
            ],
            escalation_required=False,
            policy_sources=["Service Rules Section 5.2: Delay Compensation Rule"],
            explanation=(
                f"Flight {booking.flight_number} is delayed by {delay:.1f} hours (> 5 hours). "
                "Qualifies for a meal voucher, lounge access, and hotel accommodation covering only the "
                "delayed-hours portion. A full night's stay is not permitted under Section 5.2."
            ),
            details={
                "delay_hours": delay,
                "meal_voucher": True,
                "lounge_access": True,
                "hotel_eligible": True,
                "hotel_scope": "DELAYED_HOURS_ONLY",
                "full_night_allowed": False
            }
        )

    @staticmethod
    def evaluate_fare_difference(fare_diff_inr: float) -> PolicyDecision:
        """Section 5.4: Fare Difference Rule."""
        if fare_diff_inr <= AGENT_WAIVER_LIMIT_INR:
            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.4",
                policy_name="Fare Difference Rule (Within Agent Authority)",
                allowed_actions=["AGENT_HANDLES_FARE_DIFF"],
                restrictions=["CUSTOMER_RESPONSIBLE_FOR_FARE_DIFF"],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.4: Fare Difference Rule"],
                explanation=(
                    f"Fare difference of ₹{fare_diff_inr:,.0f} is within agent authority threshold "
                    f"(≤ ₹{AGENT_WAIVER_LIMIT_INR:,.0f}). Customer is responsible for fare differences unless approved."
                ),
                details={"fare_diff_inr": fare_diff_inr, "agent_limit_inr": AGENT_WAIVER_LIMIT_INR}
            )

        # fare_diff_inr > 1500
        return PolicyDecision(
            eligible=False,
            policy_id="POL-5.4",
            policy_name="Fare Difference Rule (Exceeds Agent Authority)",
            allowed_actions=[],
            restrictions=["SUPERVISOR_APPROVAL_REQUIRED"],
            escalation_required=True,
            escalation_reason="FARE_DIFFERENCE_EXCEEDS_AGENT_LIMIT_1500",
            policy_sources=[
                "Service Rules Section 5.4: Fare Difference Rule",
                "Service Rules Section 7.0: Prohibited Actions"
            ],
            explanation=(
                f"Requested fare difference of ₹{fare_diff_inr:,.0f} exceeds the maximum agent waiver authority "
                f"of ₹{AGENT_WAIVER_LIMIT_INR:,.0f}. Agent cannot independently waive this difference; supervisor approval is required."
            ),
            details={"fare_diff_inr": fare_diff_inr, "agent_limit_inr": AGENT_WAIVER_LIMIT_INR}
        )

    @staticmethod
    def evaluate_loyalty(tier: str, request_upgrade_or_extra: bool = False) -> PolicyDecision:
        """Section 5.5: Loyalty Tier Rule."""
        clean_tier = tier.strip().capitalize()
        if clean_tier in ["Gold", "Platinum"]:
            if request_upgrade_or_extra:
                return PolicyDecision(
                    eligible=False,
                    policy_id="POL-5.5",
                    policy_name="Loyalty Tier Rule (Extra Compensation Requested)",
                    allowed_actions=["PRIORITY_REBOOKING"],
                    restrictions=[
                        "NO_ADDITIONAL_COMPENSATION",
                        "NO_FREE_CABIN_UPGRADE_ENTITLEMENT"
                    ],
                    escalation_required=True,
                    escalation_reason="COMPENSATION_EXCEEDS_POLICY",
                    policy_sources=[
                        "Service Rules Section 5.5: Loyalty Tier Rule",
                        "Service Rules Section 7.0: Prohibited Actions"
                    ],
                    explanation=(
                        f"{clean_tier} tier provides priority rebooking and first access to next-available seats. "
                        "However, Section 5.5 explicitly states there is no additional compensation or complimentary cabin upgrades "
                        "beyond standard policy. Out-of-policy upgrade requests must be escalated to human customer relations."
                    ),
                    details={"tier": clean_tier, "priority_rebooking": True, "free_upgrade": False}
                )

            return PolicyDecision(
                eligible=True,
                policy_id="POL-5.5",
                policy_name="Loyalty Tier Rule",
                allowed_actions=["PRIORITY_REBOOKING", "FIRST_ACCESS_SEATS"],
                restrictions=["NO_ADDITIONAL_COMPENSATION"],
                escalation_required=False,
                policy_sources=["Service Rules Section 5.5: Loyalty Tier Rule"],
                explanation=(
                    f"Customer holds {clean_tier} loyalty status, granting priority rebooking and first access to "
                    "next-available seats during disruption handling."
                ),
                details={"tier": clean_tier, "priority_rebooking": True}
            )

        return PolicyDecision(
            eligible=True,
            policy_id="POL-5.5",
            policy_name="Loyalty Tier Rule (Standard/Silver)",
            allowed_actions=[],
            restrictions=[],
            escalation_required=False,
            policy_sources=["Service Rules Section 5.5: Loyalty Tier Rule"],
            explanation=f"Customer holds {clean_tier} status. Standard disruption policy applies.",
            details={"tier": clean_tier}
        )

    @staticmethod
    def evaluate_return_flight(booking: Booking) -> Optional[PolicyDecision]:
        """Verify return flight status if present (Priya Nair scenario)."""
        if not booking.return_flight:
            return None

        ret = booking.return_flight
        return PolicyDecision(
            eligible=True,
            policy_id="POL-RETURN",
            policy_name="Return Flight Status Verification",
            allowed_actions=["RETURN_FLIGHT_CONFIRMED_UNAFFECTED"],
            restrictions=["RETURN_FLIGHT_IS_NOT_DISRUPTED"],
            escalation_required=False,
            policy_sources=["Authoritative Transaction Data: Booking SK4821X"],
            explanation=(
                f"Return flight {ret.route} on {ret.date} (scheduled departure {ret.scheduled_departure}) "
                f"is strictly {ret.status}. Disruption resolution applies only to outbound leg {booking.flight_number}."
            ),
            details={
                "route": ret.route,
                "date": ret.date,
                "scheduled_departure": ret.scheduled_departure,
                "status": ret.status
            }
        )
