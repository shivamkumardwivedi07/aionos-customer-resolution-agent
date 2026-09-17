"""Integration tests for FastAPI REST endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "Wednesday, 23 September 2026" in data["exercise_date"]


def test_customers_endpoint():
    res = client.get("/api/customers")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 3
    names = [c["customer"]["name"] for c in data]
    assert "Priya Nair" in names
    assert "Arvind Kulkarni" in names
    assert "Meher Kaur" in names


def test_policies_endpoint():
    res = client.get("/api/policies")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5
    policy_ids = [p["policy_id"] for p in data]
    assert "POL-5.1" in policy_ids
    assert "POL-5.2" in policy_ids
    assert "POL-5.3" in policy_ids
    assert "POL-5.4" in policy_ids
    assert "POL-5.5" in policy_ids


def test_scenarios_endpoint():
    res = client.get("/api/scenarios")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3


def test_chat_and_audit_flow():
    # 1. Reset state
    client.post("/api/reset", json={"reset_audit": True})

    # 2. Chat message
    chat_payload = {
        "message": "My flight SK-204 is cancelled. I would like a full refund please.",
        "customer_id": "CUST-001"
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["customer_name"] == "Priya Nair"
    assert any(a["action_type"] == "REFUND_REQUESTED" for a in data["actions_taken"])

    # 3. Verify audit trail
    audit_res = client.get("/api/audit")
    assert audit_res.status_code == 200
    events = audit_res.json()
    assert len(events) >= 1
    assert events[0]["pnr"] == "SK4821X"
