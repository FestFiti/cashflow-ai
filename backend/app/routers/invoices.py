import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.business import Business
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.utils.auth import get_current_business_id

router = APIRouter()


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
