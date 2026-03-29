from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import hashlib

from app.database import get_db
from app.models.business import Business
from app.models.session import Session
from app.utils.auth import get_current_business_id, get_session_id_from_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    mpesa_shortcode: str | None = None


@router.get("/")
async def get_profile(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return {
        "id": str(business.id),
        "name": business.name,
        "email": business.email,
        "phone": business.phone,
        "mpesa_shortcode": business.mpesa_shortcode,
        "created_at": business.created_at.isoformat(),
    }


@router.patch("/")
async def update_profile(
    req: UpdateProfileRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    if req.name is not None:
        business.name = req.name
    if req.phone is not None:
        business.phone = req.phone
    if req.mpesa_shortcode is not None:
        business.mpesa_shortcode = req.mpesa_shortcode

    await db.commit()
    await db.refresh(business)
    return {
        "id": str(business.id),
        "name": business.name,
        "email": business.email,
        "phone": business.phone,
        "mpesa_shortcode": business.mpesa_shortcode,
        "created_at": business.created_at.isoformat(),
    }


@router.get("/sessions")
async def list_sessions(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    current_sid = get_session_id_from_token(credentials.credentials)
    result = await db.execute(
        select(Session)
        .where(Session.business_id == business_id, Session.is_active == True)
        .order_by(Session.last_seen_at.desc())
    )
    sessions = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "device_name": s.device_name,
            "ip_address": s.ip_address,
            "created_at": s.created_at.isoformat(),
            "last_seen_at": s.last_seen_at.isoformat(),
            "is_current": str(s.id) == current_sid,
        }
        for s in sessions
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    current_sid = get_session_id_from_token(credentials.credentials)
    if session_id == current_sid:
        raise HTTPException(status_code=400, detail="Cannot revoke your current session. Use logout instead.")

    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.business_id == business_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.is_active = False
    await db.commit()
    return {"message": "Session revoked"}


@router.delete("/sessions")
async def revoke_all_other_sessions(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    current_sid = get_session_id_from_token(credentials.credentials)
    result = await db.execute(
        select(Session).where(
            Session.business_id == business_id,
            Session.is_active == True,
            Session.id != current_sid,
        )
    )
    sessions = result.scalars().all()
    for s in sessions:
        s.is_active = False
    await db.commit()
    return {"message": f"Revoked {len(sessions)} session(s)"}
