import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.utils.auth import get_current_business_id

router = APIRouter()


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    req: InvoiceCreate,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    invoice = Invoice(
        business_id=uuid.UUID(business_id),
        client_name=req.client_name,
        client_phone=req.client_phone,
        client_email=req.client_email,
        amount=req.amount,
        description=req.description,
        due_date=req.due_date,
        status="draft",
    )
    db.add(invoice)
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
