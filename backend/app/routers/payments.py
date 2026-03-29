import json
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.services.mpesa import stk_push, normalize_phone
from app.utils.auth import get_current_business_id
from app.utils.redis import redis_client

logger = logging.getLogger("payments")
router = APIRouter()


class STKPushRequest(BaseModel):
    invoice_id: str
    phone: str | None = None  # override client_phone if provided


@router.get("/")
async def list_payments(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """List recent payments for the business (via invoices)."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(Payment, Invoice.client_name)
        .join(Invoice, Payment.invoice_id == Invoice.id)
        .where(Invoice.business_id == bid)
        .order_by(Payment.created_at.desc())
        .limit(20)
    )
    rows = result.all()
    return [
        {
            "id": str(p.id),
            "client_name": client_name,
            "amount": float(p.amount),
            "status": p.status,
            "mpesa_receipt": p.mpesa_receipt,
            "phone": p.phone,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p, client_name in rows
    ]


@router.get("/stats")
async def payment_stats(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Aggregate payment stats for the business."""
    from sqlalchemy import func

    bid = uuid.UUID(business_id)
    # Total completed incoming
    incoming_result = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .join(Invoice, Payment.invoice_id == Invoice.id)
        .where(Invoice.business_id == bid, Payment.status == "completed")
    )
    incoming = float(incoming_result.scalar())

    return {
        "incoming": incoming,
        "outgoing": 0,
        "net_flow": incoming,
    }


@router.post("/stk-push")
async def initiate_stk_push(
    req: STKPushRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # Load invoice and verify ownership
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == uuid.UUID(req.invoice_id),
            Invoice.business_id == uuid.UUID(business_id),
        )
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice already paid")

    phone = req.phone or invoice.client_phone
    amount = int(invoice.amount)

    logger.info(
        "Initiating STK push — invoice=%s client=%s amount=%d phone=%s",
        invoice.id, invoice.client_name, amount, phone,
    )

    try:
        daraja_response = await stk_push(
            phone=phone,
            amount=amount,
            account_reference=str(invoice.id)[:12],
            description="Invoice payment",
        )
    except Exception as exc:
        logger.error("STK Push failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"M-Pesa request failed: {exc}")

    checkout_id = daraja_response.get("CheckoutRequestID")
    merchant_id = daraja_response.get("MerchantRequestID")

    logger.info(
        "STK Push accepted — CheckoutRequestID=%s MerchantRequestID=%s",
        checkout_id, merchant_id,
    )

    # Persist pending payment record
    payment = Payment(
        invoice_id=invoice.id,
        checkout_request_id=checkout_id,
        amount=invoice.amount,
        phone=normalize_phone(phone),
        status="pending",
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    # Cache checkout → invoice/payment mapping for webhook matching (10 min TTL)
    await redis_client.setex(
        f"mpesa:checkout:{checkout_id}",
        600,
        json.dumps({
            "invoice_id": str(invoice.id),
            "business_id": business_id,
            "payment_id": str(payment.id),
            "amount": amount,
            "client_name": invoice.client_name,
        }),
    )

    logger.info("Payment record created — payment_id=%s", payment.id)

    return {
        "status": "pending",
        "message": daraja_response.get("CustomerMessage", "STK Push sent to phone"),
        "checkout_request_id": checkout_id,
        "payment_id": str(payment.id),
    }


@router.get("/{checkout_id}/status")
async def payment_status(
    checkout_id: str,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).where(Payment.checkout_request_id == checkout_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        cached = await redis_client.get(f"mpesa:checkout:{checkout_id}")
        if cached:
            return {"checkout_id": checkout_id, "status": "pending"}
        raise HTTPException(status_code=404, detail="Payment not found")

    logger.info("Status check — checkout=%s status=%s", checkout_id, payment.status)

    return {
        "checkout_id": checkout_id,
        "payment_id": str(payment.id),
        "status": payment.status,
        "mpesa_receipt": payment.mpesa_receipt,
        "amount": float(payment.amount),
        "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
    }
