"""Anthropic Claude API wrapper for AI features.

Uses claude-haiku-4-5-20251001 (cheapest model) by default.
Model is configurable via CLAUDE_MODEL env var.
"""

import json
import anthropic

from app.config import settings

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
MODEL = settings.CLAUDE_MODEL


async def generate_invoice(prompt: str) -> dict:
    """Parse natural language into structured invoice JSON."""
    response = await client.messages.create(
        model=MODEL,
        max_tokens=512,
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
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
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

    response = await client.messages.create(
        model=MODEL,
        max_tokens=200,
        system="""Write a short, polite payment reminder SMS (under 160 chars) for a Kenyan business context.
Be professional but warm. Include the amount and due date. Return ONLY the SMS text, nothing else.""",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


async def cash_flow_insights(data: dict) -> str:
    """Generate a natural-language cash flow summary."""
    response = await client.messages.create(
        model=MODEL,
        max_tokens=300,
        system="""You are a financial analyst for a small Kenyan business.
Given their cash flow data, write 2-3 concise insights with actionable advice.
Use KES currency. Be direct and specific.""",
        messages=[
            {
                "role": "user",
                "content": f"Cash flow data:\n{json.dumps(data, indent=2)}",
            }
        ],
    )
    return response.content[0].text.strip()


async def summarise_dispute(conversation: list[str]) -> str:
    """Summarise a payment dispute conversation."""
    response = await client.messages.create(
        model=MODEL,
        max_tokens=400,
        system="""Summarise this payment dispute timeline objectively.
List key facts, each party's position, and suggest a fair resolution.
Be concise and professional.""",
        messages=[
            {
                "role": "user",
                "content": "\n---\n".join(conversation),
            }
        ],
    )
    return response.content[0].text.strip()
