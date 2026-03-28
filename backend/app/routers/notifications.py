import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from app.database import get_db
from app.models.notification import Notification
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.get("/")
async def list_notifications(
    limit: int = 20,
    unread_only: bool = False,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    bid = uuid.UUID(business_id)
    query = select(Notification).where(Notification.business_id == bid)
    if unread_only:
        query = query.where(Notification.is_read == False)  # noqa: E712
    query = query.order_by(Notification.created_at.desc()).limit(limit)
    result = await db.execute(query)
    notifications = result.scalars().all()
    return [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "category": n.category,
            "is_read": n.is_read,
            "link": n.link,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ]


@router.get("/unread-count")
async def unread_count(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    bid = uuid.UUID(business_id)
    result = await db.execute(
        select(func.count()).where(
            Notification.business_id == bid, Notification.is_read == False  # noqa: E712
        )
    )
    return {"count": result.scalar()}


@router.patch("/{notification_id}/read")
async def mark_read(
    notification_id: uuid.UUID,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(
        update(Notification)
        .where(Notification.id == notification_id, Notification.business_id == uuid.UUID(business_id))
        .values(is_read=True)
    )
    await db.commit()
    return {"status": "ok"}


@router.post("/mark-all-read")
async def mark_all_read(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(
        update(Notification)
        .where(Notification.business_id == uuid.UUID(business_id), Notification.is_read == False)  # noqa: E712
        .values(is_read=True)
    )
    await db.commit()
    return {"status": "ok"}
