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


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_active: bool | None = None


class ServiceResponse(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    name: str
    description: str | None
    price: float
    is_active: bool
    created_at: str

    model_config = {"from_attributes": True}


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
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return {
        "id": str(service.id),
        "business_id": str(service.business_id),
        "name": service.name,
        "description": service.description,
        "price": float(service.price),
        "is_active": service.is_active,
        "created_at": service.created_at.isoformat(),
    }


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
    services = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "business_id": str(s.business_id),
            "name": s.name,
            "description": s.description,
            "price": float(s.price),
            "is_active": s.is_active,
            "created_at": s.created_at.isoformat(),
        }
        for s in services
    ]


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

    if req.name is not None:
        service.name = req.name
    if req.description is not None:
        service.description = req.description
    if req.price is not None:
        service.price = req.price
    if req.is_active is not None:
        service.is_active = req.is_active

    await db.commit()
    await db.refresh(service)
    return {
        "id": str(service.id),
        "business_id": str(service.business_id),
        "name": service.name,
        "description": service.description,
        "price": float(service.price),
        "is_active": service.is_active,
        "created_at": service.created_at.isoformat(),
    }


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
