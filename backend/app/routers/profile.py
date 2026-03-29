import os
import uuid
import shutil

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.database import get_db
from app.models.business import Business
from app.models.session import Session
from app.utils.auth import get_current_business_id, get_session_id_from_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

LOGO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "logos")


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    mpesa_shortcode: str | None = None
    address: str | None = None
    city: str | None = None
    description: str | None = None


def _business_response(business: Business) -> dict:
    return {
        "id": str(business.id),
        "name": business.name,
        "email": business.email,
        "phone": business.phone,
        "mpesa_shortcode": business.mpesa_shortcode,
        "logo_url": business.logo_url,
        "address": business.address,
        "city": business.city,
        "description": business.description,
        "is_configured": bool(business.logo_url and business.address),
        "created_at": business.created_at.isoformat(),
    }


@router.get("/")
async def get_profile(
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return _business_response(business)


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
    if req.address is not None:
        business.address = req.address
    if req.city is not None:
        business.city = req.city
    if req.description is not None:
        business.description = req.description

    await db.commit()
    await db.refresh(business)
    return _business_response(business)


@router.post("/logo")
async def upload_logo(
    file: UploadFile = File(...),
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/svg+xml"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed. Use PNG, JPEG, WebP, or SVG.")

    # Determine extension from content type
    ext_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
    }
    ext = ext_map.get(file.content_type, ".png")

    os.makedirs(LOGO_DIR, exist_ok=True)

    filename = f"{business_id}{ext}"
    filepath = os.path.join(LOGO_DIR, filename)

    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    logo_url = f"/static/logos/{filename}"
    business.logo_url = logo_url
    await db.commit()
    await db.refresh(business)

    return {"logo_url": logo_url}


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
