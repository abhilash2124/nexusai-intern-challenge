import asyncio
import random
import time
from dataclasses import dataclass

# Dataclass for final result
@dataclass
class CustomerContext:
    crm_data: dict
    billing_data: dict
    ticket_data: dict
    data_complete: bool
    fetch_time_ms: float


# Mock async services
async def fetch_crm(phone: str):
    await asyncio.sleep(random.uniform(0.2, 0.4))
    return {
        "phone": phone,
        "vip": random.choice([True, False]),
        "plan": "fiber_100"
    }


async def fetch_billing(phone: str):
    await asyncio.sleep(random.uniform(0.15, 0.35))

    # 10% chance of failure
    if random.random() < 0.1:
        raise TimeoutError("Billing service timeout")

    return {
        "status": random.choice(["paid", "overdue"]),
        "last_payment": "2026-03-10"
    }


async def fetch_tickets(phone: str):
    await asyncio.sleep(random.uniform(0.1, 0.3))
    return {
        "recent_complaints": [
            "internet_down",
            "slow_speed",
            "billing_issue"
        ]
    }


# Sequential Fetch
async def fetch_sequential(phone: str):
    start = time.time()

    crm = await fetch_crm(phone)
    billing = None
    tickets = await fetch_tickets(phone)

    try:
        billing = await fetch_billing(phone)
    except Exception as e:
        print("Billing error (sequential):", e)

    end = time.time()

    return CustomerContext(
        crm_data=crm,
        billing_data=billing,
        ticket_data=tickets,
        data_complete=billing is not None,
        fetch_time_ms=(end - start) * 1000
    )


# Parallel Fetch
async def fetch_parallel(phone: str):
    start = time.time()

    results = await asyncio.gather(
        fetch_crm(phone),
        fetch_billing(phone),
        fetch_tickets(phone),
        return_exceptions=True
    )

    crm, billing, tickets = results

    if isinstance(billing, Exception):
        print("Billing error (parallel):", billing)
        billing = None

    data_complete = all([
        not isinstance(crm, Exception),
        billing is not None,
        not isinstance(tickets, Exception)
    ])

    end = time.time()

    return CustomerContext(
        crm_data=crm,
        billing_data=billing,
        ticket_data=tickets,
        data_complete=data_complete,
        fetch_time_ms=(end - start) * 1000
    )


# Run Test
async def main():
    phone = "9876543210"

    print("\n--- Sequential Fetch ---")
    seq = await fetch_sequential(phone)
    print(seq)

    print("\n--- Parallel Fetch ---")
    par = await fetch_parallel(phone)
    print(par)

    print("\nSpeed Improvement:")
    print(f"{seq.fetch_time_ms:.2f} ms → {par.fetch_time_ms:.2f} ms")


if __name__ == "__main__":
    asyncio.run(main())