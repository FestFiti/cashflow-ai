"""M-Pesa Daraja API wrapper.

OAuth token is cached in Redis with a 55-minute TTL to avoid per-request auth.
All requests and responses are logged for debugging and audit.
"""

import base64
import logging
from datetime import datetime

import httpx

from app.config import settings
from app.utils.redis import redis_client

logger = logging.getLogger("mpesa")

SANDBOX_BASE = "https://sandbox.safaricom.co.ke"
PROD_BASE = "https://api.safaricom.co.ke"


def _base_url() -> str:
    return SANDBOX_BASE if settings.MPESA_ENV == "sandbox" else PROD_BASE


def normalize_phone(phone: str) -> str:
    """Normalize Kenyan phone number to 254XXXXXXXXX format."""
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    if not phone.startswith("254"):
        phone = "254" + phone
    return phone


def _generate_password(shortcode: str, passkey: str, timestamp: str) -> str:
    """base64(shortcode + passkey + timestamp)."""
    return base64.b64encode((shortcode + passkey + timestamp).encode()).decode()


async def get_access_token() -> str:
    """Get M-Pesa OAuth access token, cached in Redis for 55 minutes."""
    cache_key = "mpesa:access_token"
    cached = await redis_client.get(cache_key)
    if cached:
        logger.debug("M-Pesa token served from cache")
        return cached

    credentials = base64.b64encode(
        f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
    ).decode()

    logger.info("Fetching new M-Pesa access token from Daraja")
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{_base_url()}/oauth/v1/generate?grant_type=client_credentials",
            headers={"Authorization": f"Basic {credentials}"},
        )
        logger.info("Token response [%s]: %s", response.status_code, response.text)
        response.raise_for_status()
        data = response.json()

    token = data["access_token"]
    await redis_client.setex(cache_key, 55 * 60, token)
    logger.info("M-Pesa access token cached (55 min TTL)")
    return token


async def stk_push(
    phone: str,
    amount: int,
    account_reference: str,
    description: str,
) -> dict:
    """Initiate M-Pesa STK Push (Lipa Na M-Pesa Online).

    Returns full Daraja response including CheckoutRequestID.
    """
    token = await get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    phone_e164 = normalize_phone(phone)
    password = _generate_password(settings.MPESA_SHORTCODE, settings.MPESA_PASSKEY, timestamp)

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_e164,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_e164,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference[:12],
        "TransactionDesc": description[:13],
    }

    logger.info(
        "STK Push → phone=%s amount=%d ref=%s callback=%s",
        phone_e164, amount, account_reference, settings.MPESA_CALLBACK_URL,
    )

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{_base_url()}/mpesa/stkpush/v1/processrequest",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
        )
        logger.info("STK Push response [%s]: %s", response.status_code, response.text)
        response.raise_for_status()
        return response.json()
