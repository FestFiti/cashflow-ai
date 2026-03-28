from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.ai import AIInvoiceRequest, AIInsightRequest
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.post("/generate-invoice")
async def generate_invoice(
    req: AIInvoiceRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: Call Claude API to parse natural language into invoice fields
    return {"message": "AI invoice generation - implementation pending", "prompt": req.prompt}


@router.post("/cash-flow-insights")
async def cash_flow_insights(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: Aggregate data, send to Claude, return insights
    return {"message": "Cash flow insights - implementation pending"}


@router.post("/draft-reminder")
async def draft_reminder(
    req: AIInsightRequest,
    business_id: str = Depends(get_current_business_id),
):
    # TODO: Claude-drafted personalised reminder message
    return {"message": "AI reminder drafting - implementation pending"}
