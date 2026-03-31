import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import date

from app.database import get_db
from app.models.invoice import Invoice
from app.models.business import Business
from app.models.notification import Notification
from app.utils.auth import get_current_business_id
from app.services.claude import draft_reminder
from app.services.email import send_email
from app.services.email_templates import _base
from app.config import settings

logger = logging.getLogger("reminders")
router = APIRouter()


class SendReminderRequest(BaseModel):
    invoice_id: str
    custom_message: str | None = None


@router.get("/overdue")
async def get_overdue_invoices(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Get all overdue and sent invoices for reminder purposes."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(Invoice)
        .where(
            Invoice.business_id == bid,
            Invoice.status.in_(["sent", "overdue"]),
        )
        .order_by(Invoice.due_date.asc())
    )
    invoices = result.scalars().all()
    return [
        {
            "id": str(inv.id),
            "client_name": inv.client_name,
            "client_phone": inv.client_phone,
            "client_email": inv.client_email,
            "amount": float(inv.amount),
            "description": inv.description,
            "due_date": inv.due_date.isoformat(),
            "status": inv.status,
            "is_overdue": inv.due_date < date.today(),
            "days_overdue": (date.today() - inv.due_date).days if inv.due_date < date.today() else 0,
        }
        for inv in invoices
    ]


@router.post("/send")
async def send_reminder(
    req: SendReminderRequest,
    background_tasks: BackgroundTasks,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Send a payment reminder email to the client."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == uuid.UUID(req.invoice_id),
            Invoice.business_id == bid,
        )
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not invoice.client_email:
        raise HTTPException(status_code=400, detail="Client has no email address on this invoice. Edit the invoice to add one.")

    # Get business info for model selection and context
    biz = await db.execute(select(Business.email, Business.name).where(Business.id == bid))
    biz_row = biz.one_or_none()
    biz_email = biz_row[0] if biz_row else None
    biz_name = biz_row[1] if biz_row else None

    days_overdue = (date.today() - invoice.due_date).days if invoice.due_date < date.today() else 0
    days_until_due = (invoice.due_date - date.today()).days if invoice.due_date >= date.today() else 0

    # Generate AI reminder or use custom
    if req.custom_message:
        reminder_text = req.custom_message
        subject = f"Payment Reminder — KES {float(invoice.amount):,.0f}"
    else:
        try:
            ai = await draft_reminder(
                client_name=invoice.client_name,
                amount=float(invoice.amount),
                due_date=invoice.due_date.strftime("%B %d, %Y"),
                business_name=biz_name,
                days_overdue=days_overdue,
                days_until_due=days_until_due,
                description=invoice.description,
                email=biz_email,
            )
            reminder_text = ai["body"]
            subject = ai["subject"]
        except Exception as e:
            logger.warning("AI reminder draft failed: %s", e)
            reminder_text = f"Hi {invoice.client_name}, this is a reminder that your invoice of KES {invoice.amount:,.0f} is due on {invoice.due_date.strftime('%B %d, %Y')}. Please arrange payment at your earliest convenience."
            subject = f"Payment Reminder — KES {float(invoice.amount):,.0f}"

    # Build reminder email
    pay_link = f"{settings.APP_URL}/pay/{invoice.id}"
    if days_overdue > 0:
        days_text = f'<div class="big-sub" style="color:#ef4444;">Overdue by {days_overdue} day{"s" if days_overdue != 1 else ""}</div>'
    else:
        days_text = f'<div class="big-sub">Due {invoice.due_date.strftime("%B %d, %Y")}</div>'

    content = f"""<div class="rule"></div>
<h2 class="h1">Payment Reminder</h2>
<p class="p">{reminder_text}</p>
<div class="big">KES {float(invoice.amount):,.0f}</div>
{days_text}
<div class="rows">
  <div class="row"><span class="row-label">Invoice</span><span class="row-val" style="font-family:monospace;font-size:13px;">#{str(invoice.id)[:8].upper()}</span></div>
  <div class="row"><span class="row-label">Description</span><span class="row-val">{invoice.description}</span></div>
</div>"""
    html = _base(
        content=content,
        footer_link=pay_link,
        footer_text="View invoice & pay now →",
        bottom_note="You received this reminder because you have an outstanding invoice.",
    )

    background_tasks.add_task(
        send_email,
        to_email=invoice.client_email,
        to_name=invoice.client_name,
        subject=subject,
        html=html,
    )

    # Create notification
    notification = Notification(
        business_id=bid,
        title="Reminder sent",
        message=f"Payment reminder sent to {invoice.client_name} for KES {float(invoice.amount):,.0f}",
        category="reminder",
        link=f"/invoices/{invoice.id}",
    )
    db.add(notification)
    await db.commit()

    logger.info("Reminder sent — invoice=%s client=%s", invoice.id, invoice.client_name)

    return {"status": "sent", "message": f"Reminder sent to {invoice.client_email}"}


@router.post("/ai-draft")
async def ai_draft(
    req: SendReminderRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Generate an AI-drafted reminder message for preview."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == uuid.UUID(req.invoice_id),
            Invoice.business_id == bid,
        )
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    biz = await db.execute(select(Business.email, Business.name).where(Business.id == bid))
    biz_row = biz.one_or_none()
    biz_email = biz_row[0] if biz_row else None
    biz_name = biz_row[1] if biz_row else None

    days_overdue = (date.today() - invoice.due_date).days if invoice.due_date < date.today() else 0
    days_until_due = (invoice.due_date - date.today()).days if invoice.due_date >= date.today() else 0

    try:
        ai = await draft_reminder(
            client_name=invoice.client_name,
            amount=float(invoice.amount),
            due_date=invoice.due_date.strftime("%B %d, %Y"),
            business_name=biz_name,
            days_overdue=days_overdue,
            days_until_due=days_until_due,
            description=invoice.description,
            email=biz_email,
        )
        return {"status": "ok", "subject": ai["subject"], "message": ai["body"]}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"AI draft failed: {str(e)}")
