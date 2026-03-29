import json
import logging
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.business import Business
from app.models.payment import Payment
from app.models.notification import Notification
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.services.mpesa import stk_push, normalize_phone
from app.services.email import send_email
from app.services.email_templates import invoice_sent_email
from app.utils.auth import get_current_business_id
from app.utils.redis import redis_client
from app.config import settings

logger = logging.getLogger("invoices")
router = APIRouter()


class PublicPayRequest(BaseModel):
    phone: str


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    req: InvoiceCreate,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # If items are provided, compute amount from items
    amount = req.amount
    if req.items:
        amount = sum(item.quantity * item.unit_price for item in req.items)
    elif amount is None:
        raise HTTPException(status_code=400, detail="Either amount or items must be provided")

    invoice = Invoice(
        business_id=uuid.UUID(business_id),
        client_name=req.client_name,
        client_phone=req.client_phone,
        client_email=req.client_email,
        amount=amount,
        description=req.description,
        due_date=req.due_date,
        status="draft",
    )
    db.add(invoice)
    await db.flush()  # Get the invoice ID before creating items

    if req.items:
        for item_data in req.items:
            item_total = item_data.quantity * item_data.unit_price
            item = InvoiceItem(
                invoice_id=invoice.id,
                service_id=item_data.service_id,
                name=item_data.name,
                description=item_data.description,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total=item_total,
            )
            db.add(item)

    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.get("/", response_model=list[InvoiceResponse])
async def list_invoices(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Invoice).where(Invoice.business_id == uuid.UUID(business_id)).order_by(Invoice.created_at.desc())
    )
    return result.scalars().all()


@router.get("/public/{invoice_id}")
async def get_public_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint - no auth required. Returns invoice + items + business branding."""
    result = await db.execute(
        select(Invoice)
        .options(selectinload(Invoice.items))
        .where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Fetch business branding info
    biz_result = await db.execute(select(Business).where(Business.id == invoice.business_id))
    business = biz_result.scalar_one_or_none()

    items = [
        {
            "id": str(item.id),
            "invoice_id": str(item.invoice_id),
            "service_id": str(item.service_id) if item.service_id else None,
            "name": item.name,
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "total": float(item.total),
        }
        for item in (invoice.items or [])
    ]

    return {
        "id": str(invoice.id),
        "client_name": invoice.client_name,
        "client_phone": invoice.client_phone,
        "client_email": invoice.client_email,
        "amount": float(invoice.amount),
        "description": invoice.description,
        "due_date": invoice.due_date.isoformat(),
        "status": invoice.status,
        "payment_url": invoice.payment_url,
        "created_at": invoice.created_at.isoformat(),
        "items": items,
        "business": {
            "name": business.name if business else None,
            "logo_url": business.logo_url if business else None,
            "address": business.address if business else None,
            "city": business.city if business else None,
            "phone": business.phone if business else None,
        } if business else None,
    }


@router.post("/public/{invoice_id}/pay")
async def public_pay_invoice(
    invoice_id: uuid.UUID,
    req: PublicPayRequest,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint - no auth required. Initiates M-Pesa STK push for an invoice."""
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice already paid")

    phone = req.phone or invoice.client_phone
    amount = int(invoice.amount)

    logger.info(
        "Public STK push — invoice=%s client=%s amount=%d phone=%s",
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

    await redis_client.setex(
        f"mpesa:checkout:{checkout_id}",
        600,
        json.dumps({
            "invoice_id": str(invoice.id),
            "business_id": str(invoice.business_id),
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


@router.get("/public/{invoice_id}/payment-status/{checkout_id}")
async def public_payment_status(
    invoice_id: uuid.UUID,
    checkout_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint - no auth required. Check payment status by checkout ID."""
    result = await db.execute(
        select(Payment).where(Payment.checkout_request_id == checkout_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        cached = await redis_client.get(f"mpesa:checkout:{checkout_id}")
        if cached:
            return {"checkout_id": checkout_id, "status": "pending"}
        raise HTTPException(status_code=404, detail="Payment not found")

    return {
        "checkout_id": checkout_id,
        "payment_id": str(payment.id),
        "status": payment.status,
        "mpesa_receipt": payment.mpesa_receipt,
        "amount": float(payment.amount),
        "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
    }


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: uuid.UUID,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.business_id == uuid.UUID(business_id))
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: uuid.UUID,
    req: InvoiceUpdate,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.business_id == uuid.UUID(business_id))
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(invoice, field, value)

    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.post("/{invoice_id}/send")
async def send_invoice(
    invoice_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Send invoice email to the client and update status to 'sent'."""
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id,
            Invoice.business_id == uuid.UUID(business_id),
        )
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not invoice.client_email:
        raise HTTPException(status_code=400, detail="Client has no email address")

    # Fetch business info for the email
    biz_result = await db.execute(select(Business).where(Business.id == invoice.business_id))
    business = biz_result.scalar_one_or_none()
    business_name = business.name if business else "Your business"

    # Build email
    amount_str = f"KES {invoice.amount:,.2f}"
    due_date_str = invoice.due_date.strftime("%B %d, %Y") if invoice.due_date else "N/A"
    subject, html = invoice_sent_email(
        client_name=invoice.client_name,
        business_name=business_name,
        amount=amount_str,
        due_date=due_date_str,
        invoice_id=str(invoice.id),
    )

    # Send email in background
    background_tasks.add_task(
        send_email,
        to_email=invoice.client_email,
        to_name=invoice.client_name,
        subject=subject,
        html=html,
    )

    # Update invoice status to sent
    invoice.status = "sent"

    # Create notification for the business
    notification = Notification(
        business_id=invoice.business_id,
        title="Invoice sent",
        message=f"Invoice #{str(invoice.id)[:8].upper()} sent to {invoice.client_name} ({invoice.client_email})",
        category="info",
        link=f"/invoices",
    )
    db.add(notification)

    await db.commit()

    return {"status": "success", "message": f"Invoice sent to {invoice.client_email}"}
