"""OpenRouter AI wrapper for AI features.

Uses free models via OpenRouter's OpenAI-compatible API.
Model is configurable via OPENROUTER_MODEL env var.
"""

import json
import httpx

from app.config import settings

BASE_URL = settings.OPENROUTER_BASE_URL
API_KEY = settings.OPENROUTER_API_KEY
MODEL = settings.OPENROUTER_MODEL

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://cashflow-ai.com",
    "X-OpenRouter-Title": "CashFlow AI",
}


async def _chat(system: str, user_message: str, max_tokens: int = 512) -> str:
    """Send a chat completion request to OpenRouter."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/chat/completions",
            headers=HEADERS,
            json={
                "model": MODEL,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


async def generate_invoice(prompt: str) -> dict:
    """Parse natural language into structured invoice JSON."""
    text = await _chat(
        system="""You are an invoice parser. Extract invoice details from natural language.
Return ONLY valid JSON with these fields:
{
  "client_name": "string",
  "client_phone": "string (Kenyan format like 0712345678, or empty)",
  "client_email": "string or null",
  "amount": number,
  "description": "string",
  "due_date": "YYYY-MM-DD"
}
If a field is unclear, make a reasonable guess. For due_date, if not specified, use 14 days from today.""",
        user_message=prompt,
        max_tokens=512,
    )
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


async def draft_reminder(
    client_name: str, amount: float, due_date: str, context: str | None = None
) -> str:
    """Generate a personalised payment reminder SMS message."""
    prompt = f"Client: {client_name}\nAmount: KES {amount:,.0f}\nDue: {due_date}"
    if context:
        prompt += f"\nContext: {context}"

    return await _chat(
        system="""Write a short, polite payment reminder SMS (under 160 chars) for a Kenyan business context.
Be professional but warm. Include the amount and due date. Return ONLY the SMS text, nothing else.""",
        user_message=prompt,
        max_tokens=200,
    )


async def cash_flow_insights(data: dict) -> str:
    """Generate a natural-language cash flow summary."""
    return await _chat(
        system="""You are a financial analyst for a small Kenyan business.
Given their cash flow data, write 2-3 concise insights with actionable advice.
Use KES currency. Be direct and specific.""",
        user_message=f"Cash flow data:\n{json.dumps(data, indent=2)}",
        max_tokens=300,
    )


async def summarise_dispute(conversation: list[str]) -> str:
    """Summarise a payment dispute conversation."""
    return await _chat(
        system="""Summarise this payment dispute timeline objectively.
List key facts, each party's position, and suggest a fair resolution.
Be concise and professional.""",
        user_message="\n---\n".join(conversation),
        max_tokens=400,
    )
