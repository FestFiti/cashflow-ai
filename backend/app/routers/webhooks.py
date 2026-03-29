import json
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.database import get_db
from app.services.email import send_email
from app.services.email_templates import _base
from app.config import settings
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.notification import Notification
from app.utils.redis import redis_client
from app.utils.ws_manager import manager

logger = logging.getLogger("webhooks")
router = APIRouter()


def _get_metadata_value(items: list, name: str):
    """Extract a value from M-Pesa CallbackMetadata items list."""
    for item in items:
        if item.get("Name") == name:
            return item.get("Value")
    return None


@router.post("/c2b")
async def mpesa_stk_callback(request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Receive M-Pesa STK Push payment callback from Daraja."""
    raw_body = await request.body()
    logger.info("M-Pesa STK callback received: %s", raw_body.decode())

    try:
        body = json.loads(raw_body)
    except Exception:
        logger.error("Failed to parse callback body")
        return {"ResultCode": 0, "ResultDesc": "Accepted"}

    callback = body.get("Body", {}).get("stkCallback", {})
    checkout_id = callback.get("CheckoutRequestID")
    result_code = callback.get("ResultCode")
    result_desc = callback.get("ResultDesc", "")

    logger.info(
        "STK callback — CheckoutRequestID=%s ResultCode=%s ResultDesc=%s",
        checkout_id, result_code, result_desc,
    )

    if not checkout_id:
        logger.warning("Callback missing CheckoutRequestID")
        return {"ResultCode": 0, "ResultDesc": "Accepted"}

    # Look up cached mapping
    cached_raw = await redis_client.get(f"mpesa:checkout:{checkout_id}")
    if not cached_raw:
        logger.warning("No cached mapping for checkout_id=%s — querying DB", checkout_id)
        result = await db.execute(
            select(Payment).where(Payment.checkout_request_id == checkout_id)
        )
        payment = result.scalar_one_or_none()
        if not payment:
            logger.error("Payment not found for checkout_id=%s", checkout_id)
            return {"ResultCode": 0, "ResultDesc": "Accepted"}
        cached = {
            "invoice_id": str(payment.invoice_id),
            "payment_id": str(payment.id),
            "business_id": None,
            "client_name": "Client",
            "amount": float(payment.amount),
        }
    else:
        cached = json.loads(cached_raw)

    payment_id = uuid.UUID(cached["payment_id"])
    invoice_id = uuid.UUID(cached["invoice_id"])
    business_id = cached.get("business_id")
    client_name = cached.get("client_name", "Client")
    amount = cached.get("amount", 0)

    if result_code != 0:
        # Payment failed or cancelled by user
        logger.info("Payment failed — ResultCode=%s Desc=%s", result_code, result_desc)
        await db.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status="failed")
        )
        await db.commit()

        if business_id:
            await manager.send_to_business(business_id, "payment_failed", {
                "invoice_id": str(invoice_id),
                "reason": result_desc,
            })
        await redis_client.delete(f"mpesa:checkout:{checkout_id}")
        return {"ResultCode": 0, "ResultDesc": "Accepted"}

    # Payment successful — extract metadata
    metadata_items = callback.get("CallbackMetadata", {}).get("Item", [])
    mpesa_receipt = _get_metadata_value(metadata_items, "MpesaReceiptNumber")
    paid_amount = _get_metadata_value(metadata_items, "Amount")
    phone_number = _get_metadata_value(metadata_items, "PhoneNumber")
    transaction_date = _get_metadata_value(metadata_items, "TransactionDate")

    logger.info(
        "Payment SUCCESS — receipt=%s amount=%s phone=%s date=%s",
        mpesa_receipt, paid_amount, phone_number, transaction_date,
    )

    now = datetime.utcnow()

    # Update payment record
    await db.execute(
        update(Payment)
        .where(Payment.id == payment_id)
        .values(
            status="completed",
            mpesa_receipt=mpesa_receipt,
            amount=paid_amount or amount,
            paid_at=now,
        )
    )

    # Mark invoice as paid
    await db.execute(
        update(Invoice)
        .where(Invoice.id == invoice_id)
        .values(status="paid")
    )

    # Create in-app notification
    if business_id:
        notification = Notification(
            business_id=uuid.UUID(business_id),
            title="Payment received",
            message=f"{client_name} paid KES {paid_amount or amount:,} — receipt {mpesa_receipt}",
            category="payment",
            link=f"/invoices/{invoice_id}",
        )
        db.add(notification)

    await db.commit()

    logger.info("Invoice %s marked as paid", invoice_id)

    # Send receipt email to client
    invoice_result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice_obj = invoice_result.scalar_one_or_none()
    if invoice_obj and invoice_obj.client_email:
        receipt_content = f"""<div class="rule"></div>
<h2 class="h1">Payment Received</h2>
<p class="p">Hi {client_name}, we've received your payment. Thank you!</p>
<div class="big">KES {paid_amount or amount:,}</div>
<div class="big-sub">Paid via M-Pesa</div>
<div class="rows">
  <div class="row"><span class="row-label">Receipt</span><span class="row-val" style="font-family:monospace;font-size:13px;">{mpesa_receipt}</span></div>
  <div class="row"><span class="row-label">Invoice</span><span class="row-val" style="font-family:monospace;font-size:13px;">#{str(invoice_id)[:8].upper()}</span></div>
  <div class="row"><span class="row-label">Description</span><span class="row-val">{invoice_obj.description}</span></div>
</div>"""
        receipt_html = _base(
            content=receipt_content,
            footer_link=f"{settings.APP_URL}/pay/{invoice_id}",
            footer_text="View invoice →",
            bottom_note="You received this because a payment was made on your invoice.",
        )
        background_tasks.add_task(
            send_email,
            to_email=invoice_obj.client_email,
            to_name=client_name,
            subject=f"Payment Received — KES {paid_amount or amount:,} (Receipt {mpesa_receipt})",
            html=receipt_html,
        )
        logger.info("Receipt email queued for %s", invoice_obj.client_email)

    # Fire WebSocket event to dashboard
    if business_id:
        await manager.send_to_business(business_id, "payment_received", {
            "invoice_id": str(invoice_id),
            "payment_id": str(payment_id),
            "amount": paid_amount or amount,
            "mpesa_receipt": mpesa_receipt,
            "client_name": client_name,
            "paid_at": now.isoformat(),
        })
        await manager.send_to_business(business_id, "dashboard_update", {})

    await redis_client.delete(f"mpesa:checkout:{checkout_id}")
    return {"ResultCode": 0, "ResultDesc": "Accepted"}


@router.post("/b2c-result")
async def mpesa_b2c_result(request: Request):
    """Receive M-Pesa B2C disbursement result callback."""
    raw_body = await request.body()
    logger.info("B2C result callback: %s", raw_body.decode())
    return {"ResultCode": 0, "ResultDesc": "Accepted"}


@router.post("/ratiba")
async def ratiba_callback(request: Request):
    """Receive Ratiba scheduled job callback."""
    raw_body = await request.body()
    logger.info("Ratiba callback: %s", raw_body.decode())
    return {"status": "received"}
