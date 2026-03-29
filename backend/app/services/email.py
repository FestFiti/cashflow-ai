import httpx
from app.config import settings

async def send_email(
    to_email: str,
    to_name: str,
    subject: str,
    html: str,
    text: str | None = None,
) -> dict:
    """Send an email via eSMS Mail API."""
    if not settings.ESMS_API_KEY:
        print(f"[EMAIL SKIP] No API key — would send '{subject}' to {to_email}")
        return {"status": "skipped"}

    payload = {
        "from": {"email": settings.ESMS_FROM_EMAIL, "name": settings.ESMS_FROM_NAME},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(
            f"{settings.ESMS_BASE_URL}/v1/emails/",
            headers={
                "Authorization": f"Bearer {settings.ESMS_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        res.raise_for_status()
        return res.json()
