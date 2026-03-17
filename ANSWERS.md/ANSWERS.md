# ANSWERS.md

## Q1: Should we query DB on partial transcripts?

We should not fully depend on partial transcripts, but we can use them intelligently. Partial transcripts can be useful for pre-fetching data and reducing latency, but they are often incomplete and may lead to incorrect intent detection. A good approach is to trigger lightweight, non-critical queries (like fetching customer profile or recent history) on partial data, while waiting for the final transcript for decision-making actions. This balances responsiveness and accuracy. The tradeoff is between speed and correctness — acting too early may lead to wrong actions, while waiting too long increases latency.

---

## Q2: Risks of auto-adding CSAT ≥ 4 to knowledge base

One risk is that incorrect or temporary solutions may get added to the knowledge base. For example, a workaround that worked once may not be generally applicable. Over time, this pollutes the knowledge base with unreliable content. To prevent this, we can require multiple confirmations (e.g., same solution receiving high CSAT multiple times) before adding it.

Another risk is outdated information. Telecom systems change frequently, and solutions may become invalid. To prevent this, we should implement periodic review or expiration of knowledge entries, ensuring only relevant and accurate information remains.

---

## Q3: Handling angry cancellation customer

The system first detects low sentiment (very negative) and intent as "service_cancellation". Based on rules, it immediately escalates to a human agent. The AI should respond politely, acknowledging frustration, for example: “I understand your frustration and I’m really sorry for the inconvenience. Let me connect you to a specialist who can resolve this quickly.”

The system should pass full context to the human agent, including customer history, repeated complaints, sentiment score, and recent interactions. This ensures the human agent can respond effectively without asking the customer to repeat information.

---

## Q4: One improvement to the system

One major improvement would be adding a feedback-driven learning loop. The system can track which AI responses lead to successful resolutions and high CSAT scores, and use this data to refine future responses. This can be implemented by storing interaction outcomes and periodically retraining or adjusting prompts.

To measure effectiveness, we can track metrics like resolution rate, average CSAT, and escalation reduction over time. If the system shows improvement in these metrics, it indicates the feature is working successfully.
