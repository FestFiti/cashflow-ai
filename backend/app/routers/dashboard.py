import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.invoice import Invoice
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    bid = uuid.UUID(business_id)

    # Total receivables (non-paid invoices)
    receivables_result = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status.in_(["draft", "sent", "overdue"])
        )
    )
    total_receivables = float(receivables_result.scalar())

    # Total paid
    paid_result = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status == "paid"
        )
    )
    total_paid = float(paid_result.scalar())

    # Overdue count
    overdue_result = await db.execute(
        select(func.count()).where(Invoice.business_id == bid, Invoice.status == "overdue")
    )
    overdue_count = overdue_result.scalar()

    # Total invoices
    total_result = await db.execute(
        select(func.count()).where(Invoice.business_id == bid)
    )
    total_invoices = total_result.scalar()

    return {
        "total_receivables": total_receivables,
        "total_paid": total_paid,
        "overdue_count": overdue_count,
        "total_invoices": total_invoices,
    }
