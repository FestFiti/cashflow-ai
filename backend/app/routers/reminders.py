from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.post("/schedule")
async def schedule_reminders(
    invoice_id: str,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: Create reminder jobs via Ratiba API
    return {"message": "Reminder scheduling - implementation pending", "invoice_id": invoice_id}


@router.delete("/{invoice_id}")
async def cancel_reminders(
    invoice_id: str,
    business_id: str = Depends(get_current_business_id),
):
    # TODO: Cancel Ratiba jobs for this invoice
    return {"message": "Reminders cancelled", "invoice_id": invoice_id}
