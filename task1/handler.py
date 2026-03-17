import asyncio
from dataclasses import dataclass
from typing import Optional
from groq import Groq
import time
import os
from dotenv import load_dotenv
# -----------------------------
# Dataclass
# -----------------------------
@dataclass
class MessageResponse:
    response_text: str
    confidence: float
    suggested_action: str
    channel_formatted_response: str
    error: Optional[str]

load_dotenv()
# -----------------------------
# Groq Client
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# AI Handler
# -----------------------------
async def handle_message(customer_message: str, customer_id: str, channel: str):

    # Empty input check
    if not customer_message.strip():
        return MessageResponse("", 0.0, "", "", "Empty message")

    system_prompt = f"""
You are a telecom customer support agent.

Customer ID: {customer_id}

Rules:
- Be polite and helpful
- Suggest clear next action
- Voice responses must be under 2 sentences
- Chat/WhatsApp can be longer
"""

    def call_ai():
        return client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message}
            ]
        )

    try:
        # ⏱ Timeout handling (10 sec)
        response = await asyncio.wait_for(
            asyncio.to_thread(call_ai),
            timeout=10
        )

    except asyncio.TimeoutError:
        return MessageResponse("", 0.0, "", "", "API timeout")

    except Exception as e:
        # 🔁 Retry once if rate limit
        if "rate_limit" in str(e).lower():
            await asyncio.sleep(2)
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(call_ai),
                    timeout=10
                )
            except Exception as retry_error:
                return MessageResponse("", 0.0, "", "", f"Retry failed: {retry_error}")
        else:
            return MessageResponse("", 0.0, "", "", str(e))

    # Extract response
    ai_text = response.choices[0].message.content

    # Channel formatting
    if channel == "voice":
        ai_text = ". ".join(ai_text.split(".")[:2])

    return MessageResponse(
        response_text=ai_text,
        confidence=0.85,
        suggested_action="follow_up",
        channel_formatted_response=ai_text,
        error=None
    )

# -----------------------------
# Test Run
# -----------------------------
async def main():
    result = await handle_message(
        "My internet is not working",
        "CUST123",
        "chat"
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())