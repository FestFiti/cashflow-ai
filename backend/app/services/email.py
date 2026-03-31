import logging
import httpx
from app.config import settings

logger = logging.getLogger("email")


async def send_email(
    to_email: str,
    to_name: str,
    subject: str,
    html: str,
    text: str | None = None,
) -> dict:
    """Send an email via eSMS Mail API."""
    if not settings.ESMS_API_KEY:
        logger.warning("[EMAIL SKIP] No API key — would send '%s' to %s", subject, to_email)
        return {"status": "skipped"}

    payload = {
        "from_": {"email": settings.ESMS_FROM_EMAIL, "name": settings.ESMS_FROM_NAME},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.post(
                f"{settings.ESMS_BASE_URL}/v1/emails/",
                headers={
                    "Authorization": f"Bearer {settings.ESMS_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            res.raise_for_status()
            data = res.json()
            logger.info("[EMAIL SENT] '%s' to %s — id=%s", subject, to_email, data.get("id", "?"))
            return data
    except Exception as e:
        logger.error("[EMAIL FAIL] '%s' to %s — %s: %s", subject, to_email, type(e).__name__, e)
        return {"status": "failed", "error": str(e)}
