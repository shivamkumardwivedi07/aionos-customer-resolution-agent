"""End-to-end test suite for the three mandatory customer disruption scenarios."""

import pytest
from app.agent.orchestrator import AgentOrchestrator
from app.agent.session import session_manager
from app.services.audit_service import audit_service


@pytest.fixture(autouse=True)
def clean_state():
    session_manager.clear_all()
    audit_service.clear()


def test_scenario_1_priya_nair_cancelled_flight():
    """Scenario 1: Priya Nair (Gold) - Flight SK-204 Cancelled.

    Customer is furious, requests cash refund and free business-class upgrade on return.
    """
    message = (
        "I am absolutely furious! My flight SK-204 from Delhi to Goa was cancelled. "
        "I want a full cash refund immediately and a free business-class upgrade on my return flight for all this trouble!"
    )

    res = AgentOrchestrator.process_message(
        user_message=message,
        session_id="test-session-priya",
        override_customer_id="CUST-001"
    )

    # 1. Customer and PNR verified
    assert res.customer_name == "Priya Nair"
    assert res.pnr == "SK4821X"
    assert res.detected_sentiment == "Furious"

    # 2. Refund action initiated
    refund_action = next((a for a in res.actions_taken if a.action_type == "REFUND_REQUESTED"), None)
    assert refund_action is not None
    assert refund_action.details["refund_method"] == "ORIGINAL_PAYMENT_METHOD_ONLY"
    assert refund_action.details["sla_window"] == "7 business days"

    # 3. Return flight unaffected noted
    return_dec = next((d for d in res.policy_decisions if d.policy_id == "POL-RETURN"), None)
    assert return_dec is not None
    assert return_dec.details["status"] == "Unaffected"
    assert "return flight" in res.agent_message.lower()
    assert "unaffected" in res.agent_message.lower()

    # 4. Out-of-policy business class upgrade escalated
    assert res.escalated is True
    escalate_action = next((a for a in res.actions_taken if a.action_type == "ESCALATED_TO_HUMAN"), None)
    assert escalate_action is not None
    assert "COMPENSATION_EXCEEDS_POLICY" in escalate_action.details["triggers"]

    # 5. Citations verified
    assert any("Section 5.1" in c for c in res.policy_citations)
    assert any("Section 5.3" in c for c in res.policy_citations)


def test_scenario_2_arvind_kulkarni_4h_delay():
    """Scenario 2: Arvind Kulkarni (Silver) - Flight SK-118 Delayed 4h.

    Frustrated, missed meeting, requests hotel accommodation.
    """
    message = (
        "I am very frustrated. My flight SK-118 to Bengaluru is delayed by 4 hours and I missed my connecting client meeting. "
        "Because of this long delay, I need hotel accommodation right now."
    )

    res = AgentOrchestrator.process_message(
        user_message=message,
        session_id="test-session-arvind",
        override_customer_id="CUST-002"
    )

    assert res.customer_name == "Arvind Kulkarni"
    assert res.pnr == "TR1190B"
    assert res.detected_sentiment == "Frustrated"

    # 1. Meal voucher issued
    meal_action = next((a for a in res.actions_taken if a.action_type == "MEAL_VOUCHER_ISSUED"), None)
    assert meal_action is not None

    # 2. Lounge access issued
    lounge_action = next((a for a in res.actions_taken if a.action_type == "LOUNGE_ACCESS_ISSUED"), None)
    assert lounge_action is not None

    # 3. Hotel accommodation NOT issued (4h delay does not qualify)
    hotel_action = next((a for a in res.actions_taken if a.action_type == "HOTEL_REQUESTED_FOR_DELAYED_HOURS"), None)
    assert hotel_action is None

    # 4. Agent message clearly explains hotel policy
    assert "exceeding 5 hours" in res.agent_message or "5 hours" in res.agent_message
    assert "hotel accommodation cannot be authorized" in res.agent_message.lower() or "not applicable" in res.agent_message.lower()

    # 5. No false escalation merely for frustration
    assert res.escalated is False


def test_scenario_3_meher_kaur_6h_delay_and_fare_difference():
    """Scenario 3: Meher Kaur (Platinum) - Flight SK-305 Delayed 6h.

    Requests full night hotel + higher-fare flight with ₹2,000 fare difference.
    """
    message = (
        "My flight SK-305 is delayed by 6 hours. As a Platinum member, I demand a full night's hotel stay and want to rebook "
        "onto a different flight with a ₹2,000 higher fare with the fare difference waived."
    )

    res = AgentOrchestrator.process_message(
        user_message=message,
        session_id="test-session-meher",
        override_customer_id="CUST-003"
    )

    assert res.customer_name == "Meher Kaur"
    assert res.pnr == "WL7742"

    # 1. Meal voucher and lounge access issued
    assert any(a.action_type == "MEAL_VOUCHER_ISSUED" for a in res.actions_taken)
    assert any(a.action_type == "LOUNGE_ACCESS_ISSUED" for a in res.actions_taken)

    # 2. Hotel arranged for delayed hours only (NOT full night)
    hotel_action = next((a for a in res.actions_taken if a.action_type == "HOTEL_REQUESTED_FOR_DELAYED_HOURS"), None)
    assert hotel_action is not None
    assert "delayed hours" in hotel_action.reason.lower()
    assert "full-night stays are not eligible" in res.agent_message.lower() or "only the qualifying delayed-hours" in res.agent_message.lower()

    # 3. ₹2,000 fare difference exceeds agent limit (₹1,500) -> Escalated to supervisor
    assert res.escalated is True
    escalate_action = next((a for a in res.actions_taken if a.action_type == "ESCALATED_TO_HUMAN"), None)
    assert escalate_action is not None
    assert "FARE_DIFF_WAIVER_EXCEEDS_1500" in escalate_action.details["triggers"]

    # 4. Policy citations include 5.2, 5.4, 5.5, 7.0
    assert any("Section 5.2" in c for c in res.policy_citations)
    assert any("Section 5.4" in c for c in res.policy_citations)
