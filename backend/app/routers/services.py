import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.database import get_db
from app.models.service import Service
from app.utils.auth import get_current_business_id

router = APIRouter()


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str | None = None
    billing_type: str = "one_time"  # one_time, recurring, hourly
    billing_cycle: str | None = None  # weekly, monthly, quarterly, yearly
    unit: str | None = None  # hour, session, project, etc.


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    billing_type: str | None = None
    billing_cycle: str | None = None
    unit: str | None = None
    is_active: bool | None = None


def _service_dict(s: Service) -> dict:
    return {
        "id": str(s.id),
        "business_id": str(s.business_id),
        "name": s.name,
        "description": s.description,
        "price": float(s.price),
        "category": s.category,
        "billing_type": s.billing_type,
        "billing_cycle": s.billing_cycle,
        "unit": s.unit,
        "is_active": s.is_active,
        "created_at": s.created_at.isoformat(),
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(
    req: ServiceCreate,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    service = Service(
        business_id=uuid.UUID(business_id),
        name=req.name,
        description=req.description,
        price=req.price,
        category=req.category,
        billing_type=req.billing_type,
        billing_cycle=req.billing_cycle,
        unit=req.unit,
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return _service_dict(service)


@router.get("/")
async def list_services(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service)
        .where(Service.business_id == uuid.UUID(business_id), Service.is_active == True)
        .order_by(Service.created_at.desc())
    )
    return [_service_dict(s) for s in result.scalars().all()]


@router.patch("/{service_id}")
async def update_service(
    service_id: uuid.UUID,
    req: ServiceUpdate,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service).where(Service.id == service_id, Service.business_id == uuid.UUID(business_id))
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(service, field, value)

    await db.commit()
    await db.refresh(service)
    return _service_dict(service)


@router.delete("/{service_id}")
async def delete_service(
    service_id: uuid.UUID,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Service).where(Service.id == service_id, Service.business_id == uuid.UUID(business_id))
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.is_active = False
    await db.commit()
    return {"message": "Service deleted"}
