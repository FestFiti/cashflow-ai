import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.schemas.team import InviteUserRequest, UserResponse, UpdateRoleRequest
from app.utils.auth import get_current_business_id, hash_password

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def list_team_members(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.business_id == uuid.UUID(business_id)).order_by(User.created_at)
    )
    return result.scalars().all()


@router.post("/invite", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    req: InviteUserRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    # Check caller is owner or manager
    # TODO: Verify role from JWT claims

    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        business_id=uuid.UUID(business_id),
        email=req.email,
        name=req.name,
        phone=req.phone,
        role=req.role,
        password_hash=hash_password(req.temporary_password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_role(
    user_id: uuid.UUID,
    req: UpdateRoleRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.id == user_id, User.business_id == uuid.UUID(business_id))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "owner":
        raise HTTPException(status_code=403, detail="Cannot change owner role")
    user.role = req.role
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    user_id: uuid.UUID,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.id == user_id, User.business_id == uuid.UUID(business_id))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "owner":
        raise HTTPException(status_code=403, detail="Cannot remove owner")
    await db.delete(user)
    await db.commit()
