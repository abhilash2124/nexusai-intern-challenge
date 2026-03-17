import pytest
from decision_engine import should_escalate, CustomerContext


def create_context(vip=False, billing="paid", complaints=None, complete=True):
    return CustomerContext(
        crm_data={"vip": vip},
        billing_data={"status": billing} if billing else None,
        ticket_data={"recent_complaints": complaints or []},
        data_complete=complete,
        fetch_time_ms=100
    )


def test_low_confidence():
    """Rule 1: confidence < 0.65"""
    ctx = create_context()
    result = should_escalate(ctx, 0.5, 0, "general")
    assert result == (True, "low_confidence")


def test_angry_customer():
    """Rule 2: sentiment < -0.6"""
    ctx = create_context()
    result = should_escalate(ctx, 0.9, -0.8, "general")
    assert result == (True, "angry_customer")


def test_repeat_complaint():
    """Rule 3: repeated intent"""
    ctx = create_context(complaints=["internet", "internet", "internet"])
    result = should_escalate(ctx, 0.9, 0, "internet")
    assert result == (True, "repeat_complaint")


def test_service_cancellation():
    """Rule 4: always escalate"""
    ctx = create_context()
    result = should_escalate(ctx, 0.9, 0, "service_cancellation")
    assert result == (True, "service_cancellation")


def test_vip_billing_issue():
    """Rule 5: VIP + overdue"""
    ctx = create_context(vip=True, billing="overdue")
    result = should_escalate(ctx, 0.9, 0, "general")
    assert result == (True, "vip_billing_issue")


def test_incomplete_data():
    """Rule 6: incomplete + low confidence"""
    ctx = create_context(complete=False)
    result = should_escalate(ctx, 0.7, 0, "general")
    assert result == (True, "incomplete_data")


def test_no_escalation():
    """Normal case"""
    ctx = create_context()
    result = should_escalate(ctx, 0.9, 0, "general")
    assert result == (False, "no_escalation")


def test_edge_case_boundary():
    """Edge case: confidence exactly 0.65"""
    ctx = create_context()
    result = should_escalate(ctx, 0.65, 0, "general")
    assert result == (False, "no_escalation")