import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.invoice import Invoice
from app.models.business import Business
from app.models.service import Service
from app.schemas.ai import AIInvoiceRequest, AIInsightRequest
from app.services.claude import generate_invoice, generate_service, draft_reminder, cash_flow_insights
from app.utils.auth import get_current_business_id

router = APIRouter()


async def _get_email(business_id: str, db: AsyncSession) -> str | None:
    """Fetch the business email for model selection."""
    result = await db.execute(select(Business.email).where(Business.id == uuid.UUID(business_id)))
    return result.scalar_one_or_none()


@router.post("/generate-invoice")
async def ai_generate_invoice(
    req: AIInvoiceRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    email = await _get_email(business_id, db)

    # Fetch business services to help AI match
    result = await db.execute(
        select(Service).where(
            Service.business_id == uuid.UUID(business_id),
            Service.is_active == True,
        )
    )
    services = [
        {"name": s.name, "price": float(s.price), "id": str(s.id)}
        for s in result.scalars().all()
    ]

    try:
        invoice_data = await generate_invoice(req.prompt, services=services or None, email=email)
        return {"status": "ok", "invoice": invoice_data, "services": services}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"AI parsing failed: {str(e)}")


@router.post("/generate-service")
async def ai_generate_service(
    req: AIInvoiceRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    email = await _get_email(business_id, db)

    try:
        service_data = await generate_service(req.prompt, email=email)
        return {"status": "ok", "service": service_data}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"AI service generation failed: {str(e)}")


@router.post("/draft-reminder")
async def ai_draft_reminder(
    req: AIInsightRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    email = await _get_email(business_id, db)

    try:
        message = await draft_reminder(
            client_name=req.client_name or "Client",
            amount=req.amount or 0,
            due_date=req.due_date or "N/A",
            context=req.context,
            email=email,
        )
        return {"status": "ok", "message": message}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"AI drafting failed: {str(e)}")


@router.post("/cash-flow-insights")
async def ai_cash_flow_insights(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    bid = uuid.UUID(business_id)
    email = await _get_email(business_id, db)

    receivables = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status.in_(["draft", "sent", "overdue"])
        )
    )
    paid = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status == "paid"
        )
    )
    overdue = await db.execute(
        select(func.count()).where(Invoice.business_id == bid, Invoice.status == "overdue")
    )
    total = await db.execute(
        select(func.count()).where(Invoice.business_id == bid)
    )

    data = {
        "total_receivables": float(receivables.scalar()),
        "total_paid": float(paid.scalar()),
        "overdue_count": overdue.scalar(),
        "total_invoices": total.scalar(),
    }

    try:
        insights = await cash_flow_insights(data, email=email)
        return {"status": "ok", "insights": insights, "data": data}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"AI insights failed: {str(e)}")
