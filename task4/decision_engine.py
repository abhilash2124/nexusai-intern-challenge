from dataclasses import dataclass
from typing import List, Tuple

# Customer Context (from Task 3)
@dataclass
class CustomerContext:
    crm_data: dict
    billing_data: dict
    ticket_data: dict
    data_complete: bool
    fetch_time_ms: float


# Escalation Logic
def should_escalate(
    context: CustomerContext,
    confidence_score: float,
    sentiment_score: float,
    intent: str
) -> Tuple[bool, str]:

    # Rule 4: service cancellation → always escalate
    if intent == "service_cancellation":
        return True, "service_cancellation"

    # Rule 1: low confidence
    if confidence_score < 0.65:
        return True, "low_confidence"

    # Rule 2: angry customer
    if sentiment_score < -0.6:
        return True, "angry_customer"

    # Rule 3: repeated complaints
    complaints = context.ticket_data.get("recent_complaints", [])
    if complaints.count(intent) >= 3:
        return True, "repeat_complaint"

    # Rule 5: VIP + billing overdue
    is_vip = context.crm_data.get("vip", False)
    billing_status = context.billing_data.get("status") if context.billing_data else None

    if is_vip and billing_status == "overdue":
        return True, "vip_billing_issue"

    # Rule 6: incomplete data + low confidence
    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    return False, "no_escalation"


# Test Run
def main():
    context = CustomerContext(
        crm_data={"vip": True},
        billing_data={"status": "overdue"},
        ticket_data={"recent_complaints": ["internet_down", "internet_down", "internet_down"]},
        data_complete=True,
        fetch_time_ms=300
    )

    result = should_escalate(
        context=context,
        confidence_score=0.6,
        sentiment_score=-0.7,
        intent="internet_down"
    )

    print("Escalate:", result)


if __name__ == "__main__":
    main()