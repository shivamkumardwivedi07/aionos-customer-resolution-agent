"""Unit tests for Escalation Engine."""

from app.agent.escalation import EscalationEngine


def test_escalation_legal_threat():
    dec = EscalationEngine.evaluate(
        user_message="If you don't resolve this I will hire a lawyer and sue in consumer court!",
        detected_intents=["LEGAL_ESCALATION"],
        extracted_entities={}
    )
    assert dec.escalate is True
    assert "LEGAL_ACTION_THREAT" in dec.triggers
    assert dec.recommended_action == "ESCALATE_TO_HUMAN_SUPERVISOR"


def test_escalation_formal_complaint():
    dec = EscalationEngine.evaluate(
        user_message="I will file a formal complaint with the DGCA grievance officer.",
        detected_intents=["FORMAL_COMPLAINT"],
        extracted_entities={}
    )
    assert dec.escalate is True
    assert "FORMAL_COMPLAINT_THREAT" in dec.triggers


def test_escalation_different_payment_method():
    dec = EscalationEngine.evaluate(
        user_message="Refund the amount to a different card please.",
        detected_intents=["REFUND_REQUEST"],
        extracted_entities={"wants_different_payment_method": True}
    )
    assert dec.escalate is True
    assert "DIFFERENT_PAYMENT_METHOD_REQUEST" in dec.triggers


def test_escalation_fare_diff_exceeds_1500():
    dec = EscalationEngine.evaluate(
        user_message="Waive the ₹2,000 fare difference for my new flight.",
        detected_intents=["FARE_DIFFERENCE_REQUEST"],
        extracted_entities={"fare_difference_inr": 2000.0}
    )
    assert dec.escalate is True
    assert "FARE_DIFF_WAIVER_EXCEEDS_1500" in dec.triggers


def test_escalation_out_of_policy_upgrade():
    dec = EscalationEngine.evaluate(
        user_message="Give me a free business-class upgrade on my return flight.",
        detected_intents=["UPGRADE_REQUEST"],
        extracted_entities={"requests_cabin_upgrade": True}
    )
    assert dec.escalate is True
    assert "COMPENSATION_EXCEEDS_POLICY" in dec.triggers


def test_no_escalation_for_normal_inquiry():
    dec = EscalationEngine.evaluate(
        user_message="Can you tell me the current status of my flight SK-118?",
        detected_intents=["STATUS_INFORMATION"],
        extracted_entities={}
    )
    assert dec.escalate is False
    assert len(dec.triggers) == 0
