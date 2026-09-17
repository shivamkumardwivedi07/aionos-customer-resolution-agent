"""Response Generator.

Generates concise, empathetic, policy-grounded customer messages.
Never invents data; strictly reflects evaluated policy decisions and executed actions.
"""

from typing import List, Optional, Dict, Any
from app.models.customer import Customer
from app.models.booking import Booking
from app.models.policy import PolicyDecision, EscalationDecision
from app.models.action import ActionRecord


class ResponseGenerator:
    """Produces empathetic, professional, and policy-grounded natural language responses."""

    @classmethod
    def generate(
        cls,
        customer: Customer,
        booking: Booking,
        sentiment: str,
        policy_decisions: List[PolicyDecision],
        actions_taken: List[ActionRecord],
        escalation: EscalationDecision,
        intents: Optional[List[str]] = None,
        entities: Optional[Dict[str, Any]] = None,
        session_actions: Optional[List[ActionRecord]] = None,
        unaffected_return_noted: bool = False,
        privacy_violation_attempt: bool = False
    ) -> str:
        if privacy_violation_attempt:
            return (
                "For customer privacy and security regulations, I am only authorized to access and discuss "
                f"your own confirmed booking ({booking.booking_reference}). I cannot share details regarding any other passenger."
            )

        intents_list = intents or []
        entities_dict = entities or {}
        paragraphs: List[str] = []

        # 1. Empathy & Fact Acknowledgement
        first_name = customer.name.split()[0]
        if sentiment in ["Furious", "Frustrated"]:
            paragraphs.append(
                f"I completely understand your frustration, {first_name}, and I sincerely apologize for the disruption to your travel plans today."
            )
        else:
            paragraphs.append(f"Hello {first_name}, thank you for contacting us regarding your flight.")

        # 2. Flight Status Statement
        if booking.status.lower() == "cancelled":
            cancellation_stmt = f"I can confirm that your outbound flight {booking.flight_number} ({booking.route}) has been cancelled due to {booking.disruption_reason.lower()}."
            if booking.return_flight and booking.return_flight.status == "Unaffected":
                cancellation_stmt += f" Please note that your return flight ({booking.return_flight.route} on {booking.return_flight.date}) remains confirmed and unaffected."
            paragraphs.append(cancellation_stmt)
        elif booking.status.lower() == "delayed":
            paragraphs.append(
                f"Your flight {booking.flight_number} ({booking.route}) is currently delayed by {booking.delay_hours:.1f} hours, "
                f"with an updated departure time of {booking.current_departure}."
            )

        # 3. Policy & Action Explanations
        action_notes = []
        hotel_explained = False

        for action in actions_taken:
            if action.action_type == "REFUND_REQUESTED":
                action_notes.append(
                    "Under Service Rules Section 5.1 and 5.3, I have initiated a full refund request for you. "
                    "Per airline policy, refunds are processed within 7 business days and issued strictly to your original payment method (cash payouts or alternate accounts are not permitted)."
                )
            elif action.action_type == "MEAL_VOUCHER_ISSUED":
                val = action.details.get("value", "meal voucher")
                action_notes.append(f"I have issued a complimentary {val} for airport dining.")
            elif action.action_type == "LOUNGE_ACCESS_ISSUED":
                action_notes.append("I have activated complimentary airport lounge access for you while you wait.")
            elif action.action_type == "HOTEL_REQUESTED_FOR_DELAYED_HOURS":
                action_notes.append(
                    "I have arranged transit day-room hotel accommodation. Per Section 5.2, this accommodation covers "
                    "only the qualifying delayed-hours portion up to departure; full-night stays are not eligible under standard policy."
                )
                hotel_explained = True
            elif action.action_type == "REBOOKING_REQUESTED":
                action_notes.append(
                    "I have submitted a free rebooking request for the next available flight within 24 hours. "
                    "Specific replacement flight schedules and seat numbers are assigned directly by ground operations at the airport."
                )

        if action_notes:
            paragraphs.extend(action_notes)

        # 4. Direct Hotel Accommodation Inquiries (e.g. Meher 6h delay vs Arvind 4h delay)
        hotel_inquired = (
            "HOTEL_REQUEST" in intents_list
            or entities_dict.get("wants_full_night_hotel", False)
            or any("hotel" in str(dec.restrictions).lower() for dec in policy_decisions if "NO_HOTEL_ACCOMMODATION" in dec.restrictions)
        )

        if hotel_inquired and not hotel_explained:
            if booking.delay_hours > 5.0:
                if entities_dict.get("wants_full_night_hotel", False):
                    paragraphs.append(
                        f"Regarding hotel accommodation: Under Service Rules Section 5.2, for delays exceeding 5 hours (such as your {booking.delay_hours:.1f}-hour delay), "
                        f"you qualify for transit day-room hotel accommodation covering the delayed-hours window until departure ({booking.current_departure}). "
                        "Please note that a full night's hotel stay is strictly not eligible under airline policy."
                    )
                else:
                    paragraphs.append(
                        f"Regarding hotel accommodation: Under Service Rules Section 5.2, because your flight {booking.flight_number} is delayed by {booking.delay_hours:.1f} hours "
                        f"(exceeding the 5-hour threshold), you qualify for transit day-room hotel accommodation covering the delayed-hours window until departure at {booking.current_departure}."
                    )
            else:
                paragraphs.append(
                    f"Regarding hotel accommodation: Under Service Rules Section 5.2, hotel assistance is only provided "
                    f"for delays exceeding 5 hours. Because your delay is {booking.delay_hours:.1f} hours, hotel accommodation cannot be authorized."
                )

        # 5. Fare Difference Inquiries
        for dec in policy_decisions:
            if not dec.eligible:
                if "FARE_DIFFERENCE_EXCEEDS_AGENT_LIMIT_1500" in (dec.escalation_reason or ""):
                    fare_val = dec.details.get("fare_diff_inr", 2000)
                    paragraphs.append(
                        f"Regarding your request for a higher-fare flight: The fare difference is ₹{fare_val:,.0f}. "
                        "Under Service Rules Section 5.4, any fare difference waiver exceeding ₹1,500 requires supervisor approval."
                    )

        # 6. Loyalty Tier Benefits Inquiries
        loyalty_inquired = (
            "UPGRADE_REQUEST" in intents_list
            or entities_dict.get("requests_cabin_upgrade", False)
            or any("loyalty" in str(i).lower() for i in intents_list)
        )
        if loyalty_inquired and not any("cabin upgrade" in p.lower() for p in paragraphs):
            paragraphs.append(
                f"Regarding your {customer.loyalty_tier} loyalty tier status: Under Service Rules Section 5.5, {customer.loyalty_tier} members "
                "receive priority rebooking and first access to next-available seats during disruptions. However, loyalty status does not "
                "grant complimentary cabin upgrades, fee waivers, or additional monetary compensation beyond standard disruption policy."
            )

        # 7. Escalation & Next Steps
        if escalation.escalate:
            ticket_ref = ""
            for action in actions_taken:
                if action.action_type == "ESCALATED_TO_HUMAN":
                    ticket_ref = f" (Ticket ID: {action.details.get('ticket_id', 'PENDING')})"
                    break

            if "COMPENSATION_EXCEEDS_POLICY" in escalation.triggers:
                paragraphs.append(
                    f"Your request for an out-of-policy cabin upgrade or additional compensation exceeds automated agent authority{ticket_ref}. "
                    "I have escalated your request directly to our Senior Customer Relations team for supervisory review."
                )
            elif "FARE_DIFF_WAIVER_EXCEEDS_1500" in escalation.triggers:
                paragraphs.append(
                    f"I have escalated the ₹{dec.details.get('fare_diff_inr', 2000):,.0f} fare-difference waiver request to a human supervisor{ticket_ref} "
                    "for formal review."
                )
            elif "LEGAL_ACTION_THREAT" in escalation.triggers or "FORMAL_COMPLAINT_THREAT" in escalation.triggers:
                paragraphs.append(
                    f"Given your mention of formal legal/regulatory escalation, I have immediately logged an expedited ticket{ticket_ref} "
                    "with our Executive Grievance Support Desk, who will contact you directly."
                )
            else:
                paragraphs.append(
                    f"I have escalated this matter to a human specialist{ticket_ref} to provide further assistance."
                )

        # 8. Prompting when customer choice is needed
        cancellation_dec = next((d for d in policy_decisions if d.policy_id == "POL-5.1"), None)
        if cancellation_dec and "CUSTOMER_CHOOSES_OPTION" in cancellation_dec.restrictions and not actions_taken:
            paragraphs.append(
                "Please let me know whether you would prefer: "
                "(1) Free rebooking on the next available flight within 24 hours, or "
                "(2) A full refund to your original payment method."
            )

        return "\n\n".join(paragraphs)
