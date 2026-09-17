"""Unit tests for Deterministic Policy Engine."""

import pytest
from app.models.booking import Booking, ReturnFlight
from app.agent.policy_engine import PolicyEngine


@pytest.fixture
def priya_booking():
    return Booking(
        booking_reference="SK4821X",
        customer_id="CUST-001",
        customer_name="Priya Nair",
        flight_number="SK-204",
        route="Delhi → Goa",
        date="Wednesday, 23 September 2026",
        scheduled_departure="18:40",
        original_departure="18:40",
        current_departure=None,
        status="Cancelled",
        disruption_reason="Operational reasons",
        delay_hours=0.0,
        return_flight=ReturnFlight(
            route="Goa → Delhi",
            date="Friday, 25 September 2026",
            scheduled_departure="16:20",
            status="Unaffected"
        )
    )


@pytest.fixture
def arvind_booking():
    return Booking(
        booking_reference="TR1190B",
        customer_id="CUST-002",
        customer_name="Arvind Kulkarni",
        flight_number="SK-118",
        route="Mumbai → Bengaluru",
        date="Wednesday, 23 September 2026",
        scheduled_departure="07:10",
        original_departure="07:10",
        current_departure="11:10",
        status="Delayed",
        disruption_reason="Operational delay",
        delay_hours=4.0,
        return_flight=None
    )


@pytest.fixture
def meher_booking():
    return Booking(
        booking_reference="WL7742",
        customer_id="CUST-003",
        customer_name="Meher Kaur",
        flight_number="SK-305",
        route="Delhi → Hyderabad",
        date="Wednesday, 23 September 2026",
        scheduled_departure="14:00",
        original_departure="14:00",
        current_departure="20:00",
        status="Delayed",
        disruption_reason="Operational delay",
        delay_hours=6.0,
        return_flight=None
    )


def test_cancellation_refund_rule(priya_booking):
    dec = PolicyEngine.evaluate_cancellation(priya_booking, chosen_action="REFUND")
    assert dec.eligible is True
    assert "FULL_REFUND" in dec.allowed_actions
    assert "ORIGINAL_PAYMENT_METHOD_ONLY" in dec.restrictions
    assert "PROCESSED_WITHIN_7_BUSINESS_DAYS" in dec.restrictions
    assert dec.escalation_required is False


def test_cancellation_rebooking_rule(priya_booking):
    dec = PolicyEngine.evaluate_cancellation(priya_booking, chosen_action="REBOOK")
    assert dec.eligible is True
    assert "FREE_REBOOKING_24H" in dec.allowed_actions
    assert "NO_FABRICATED_INVENTORY" in dec.restrictions


def test_return_flight_unaffected(priya_booking):
    dec = PolicyEngine.evaluate_return_flight(priya_booking)
    assert dec is not None
    assert dec.eligible is True
    assert dec.details["status"] == "Unaffected"
    assert "Unaffected" in dec.explanation


def test_delay_compensation_4h_arvind(arvind_booking):
    dec = PolicyEngine.evaluate_delay_compensation(arvind_booking)
    assert dec.eligible is True
    assert "MEAL_VOUCHER" in dec.allowed_actions
    assert "LOUNGE_ACCESS" in dec.allowed_actions
    assert "NO_HOTEL_ACCOMMODATION" in dec.restrictions
    assert dec.details["hotel_eligible"] is False


def test_delay_compensation_6h_meher(meher_booking):
    dec = PolicyEngine.evaluate_delay_compensation(meher_booking)
    assert dec.eligible is True
    assert "MEAL_VOUCHER" in dec.allowed_actions
    assert "LOUNGE_ACCESS" in dec.allowed_actions
    assert "HOTEL_ACCOMMODATION_DELAYED_HOURS_ONLY" in dec.allowed_actions
    assert "HOTEL_COVERS_DELAYED_HOURS_ONLY" in dec.restrictions
    assert "NO_FULL_NIGHT_STAY" in dec.restrictions
    assert dec.details["full_night_allowed"] is False


def test_fare_difference_within_limit():
    dec = PolicyEngine.evaluate_fare_difference(1200.0)
    assert dec.eligible is True
    assert dec.escalation_required is False


def test_fare_difference_exceeds_limit():
    dec = PolicyEngine.evaluate_fare_difference(2000.0)
    assert dec.eligible is False
    assert dec.escalation_required is True
    assert dec.escalation_reason == "FARE_DIFFERENCE_EXCEEDS_AGENT_LIMIT_1500"


def test_loyalty_tier_no_extra_compensation():
    dec = PolicyEngine.evaluate_loyalty(tier="Platinum", request_upgrade_or_extra=True)
    assert dec.eligible is False
    assert dec.escalation_required is True
    assert "NO_ADDITIONAL_COMPENSATION" in dec.restrictions
