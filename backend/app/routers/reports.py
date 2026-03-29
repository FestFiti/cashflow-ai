import uuid
from datetime import datetime, timedelta, timezone, date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, extract, and_

from app.database import get_db
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.get("/overview")
async def reports_overview(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """High-level stats for the reports dashboard."""
    bid = uuid.UUID(business_id)
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    # All-time totals
    total_invoiced = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(Invoice.business_id == bid)
    )
    total_collected = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status == "paid"
        )
    )
    total_outstanding = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status.in_(["sent", "overdue"])
        )
    )
    overdue_amount = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.status == "overdue"
        )
    )

    # Counts
    invoice_count = await db.execute(
        select(func.count()).where(Invoice.business_id == bid)
    )
    paid_count = await db.execute(
        select(func.count()).where(Invoice.business_id == bid, Invoice.status == "paid")
    )
    overdue_count = await db.execute(
        select(func.count()).where(Invoice.business_id == bid, Invoice.status == "overdue")
    )

    # Last 30 days
    invoiced_30d = await db.execute(
        select(func.coalesce(func.sum(Invoice.amount), 0)).where(
            Invoice.business_id == bid, Invoice.created_at >= thirty_days_ago
        )
    )
    collected_30d = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.status == "completed",
            Payment.paid_at >= thirty_days_ago,
            Payment.invoice_id.in_(select(Invoice.id).where(Invoice.business_id == bid)),
        )
    )

    ti = float(total_invoiced.scalar())
    tc = float(total_collected.scalar())

    return {
        "total_invoiced": ti,
        "total_collected": tc,
        "total_outstanding": float(total_outstanding.scalar()),
        "overdue_amount": float(overdue_amount.scalar()),
        "invoice_count": invoice_count.scalar(),
        "paid_count": paid_count.scalar(),
        "overdue_count": overdue_count.scalar(),
        "collection_rate": round((tc / ti) * 100, 1) if ti > 0 else 0,
        "invoiced_30d": float(invoiced_30d.scalar()),
        "collected_30d": float(collected_30d.scalar()),
    }


@router.get("/revenue-chart")
async def revenue_chart(
    months: int = Query(6, ge=1, le=12),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Monthly invoiced vs collected for the last N months."""
    bid = uuid.UUID(business_id)
    now = datetime.now(timezone.utc)
    results = []

    for i in range(months - 1, -1, -1):
        # Calculate month boundaries
        dt = now - timedelta(days=i * 30)
        month_start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        invoiced = await db.execute(
            select(func.coalesce(func.sum(Invoice.amount), 0)).where(
                Invoice.business_id == bid,
                Invoice.created_at >= month_start,
                Invoice.created_at < month_end,
            )
        )
        collected = await db.execute(
            select(func.coalesce(func.sum(Payment.amount), 0)).where(
                Payment.status == "completed",
                Payment.paid_at >= month_start,
                Payment.paid_at < month_end,
                Payment.invoice_id.in_(select(Invoice.id).where(Invoice.business_id == bid)),
            )
        )
        results.append({
            "month": month_start.strftime("%b %Y"),
            "invoiced": float(invoiced.scalar()),
            "collected": float(collected.scalar()),
        })

    return results


@router.get("/status-breakdown")
async def status_breakdown(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Invoice count and amount by status."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(
            Invoice.status,
            func.count().label("count"),
            func.coalesce(func.sum(Invoice.amount), 0).label("amount"),
        )
        .where(Invoice.business_id == bid)
        .group_by(Invoice.status)
    )
    rows = result.all()
    return [{"status": r.status, "count": r.count, "amount": float(r.amount)} for r in rows]


@router.get("/top-clients")
async def top_clients(
    limit: int = Query(10, ge=1, le=50),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Top clients by total invoiced amount."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(
            Invoice.client_name,
            func.count().label("invoice_count"),
            func.coalesce(func.sum(Invoice.amount), 0).label("total_amount"),
            func.coalesce(
                func.sum(case((Invoice.status == "paid", Invoice.amount), else_=0)), 0
            ).label("paid_amount"),
        )
        .where(Invoice.business_id == bid)
        .group_by(Invoice.client_name)
        .order_by(func.sum(Invoice.amount).desc())
        .limit(limit)
    )
    rows = result.all()
    return [
        {
            "client_name": r.client_name,
            "invoice_count": r.invoice_count,
            "total_amount": float(r.total_amount),
            "paid_amount": float(r.paid_amount),
            "collection_rate": round((float(r.paid_amount) / float(r.total_amount)) * 100, 1)
            if float(r.total_amount) > 0
            else 0,
        }
        for r in rows
    ]


@router.get("/aging")
async def aging_report(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Receivables aging buckets."""
    bid = uuid.UUID(business_id)
    today = date.today()

    result = await db.execute(
        select(Invoice).where(
            Invoice.business_id == bid, Invoice.status.in_(["sent", "overdue"])
        )
    )
    invoices = result.scalars().all()

    buckets = {
        "current": {"count": 0, "amount": 0.0, "label": "Current"},
        "1_30": {"count": 0, "amount": 0.0, "label": "1-30 days"},
        "31_60": {"count": 0, "amount": 0.0, "label": "31-60 days"},
        "61_90": {"count": 0, "amount": 0.0, "label": "61-90 days"},
        "90_plus": {"count": 0, "amount": 0.0, "label": "90+ days"},
    }

    for inv in invoices:
        days_past = (today - inv.due_date).days
        amt = float(inv.amount)
        if days_past <= 0:
            buckets["current"]["count"] += 1
            buckets["current"]["amount"] += amt
        elif days_past <= 30:
            buckets["1_30"]["count"] += 1
            buckets["1_30"]["amount"] += amt
        elif days_past <= 60:
            buckets["31_60"]["count"] += 1
            buckets["31_60"]["amount"] += amt
        elif days_past <= 90:
            buckets["61_90"]["count"] += 1
            buckets["61_90"]["amount"] += amt
        else:
            buckets["90_plus"]["count"] += 1
            buckets["90_plus"]["amount"] += amt

    return list(buckets.values())


@router.get("/recent-payments")
async def recent_payments(
    limit: int = Query(10, ge=1, le=50),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    """Recent completed payments."""
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(Payment, Invoice.client_name)
        .join(Invoice, Payment.invoice_id == Invoice.id)
        .where(Invoice.business_id == bid, Payment.status == "completed")
        .order_by(Payment.paid_at.desc())
        .limit(limit)
    )
    rows = result.all()
    return [
        {
            "id": str(p.id),
            "client_name": client_name,
            "amount": float(p.amount),
            "mpesa_receipt": p.mpesa_receipt,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
        }
        for p, client_name in rows
    ]
