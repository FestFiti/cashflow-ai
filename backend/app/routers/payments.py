from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.post("/stk-push")
async def initiate_stk_push(
    invoice_id: str,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: Implement M-Pesa STK Push via Daraja API
    return {"message": "STK Push endpoint - implementation pending", "invoice_id": invoice_id}


@router.get("/{checkout_id}/status")
async def payment_status(
    checkout_id: str,
    business_id: str = Depends(get_current_business_id),
):
    # TODO: Query payment status from Redis/DB
    return {"checkout_id": checkout_id, "status": "pending"}
