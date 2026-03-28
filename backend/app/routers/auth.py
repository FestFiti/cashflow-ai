from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.business import Business
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    TokenResponse,
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    decode_reset_token,
    get_current_business_id,
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Business).where(Business.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    business = Business(
        name=req.name,
        email=req.email,
        phone=req.phone,
        password_hash=hash_password(req.password),
    )
    db.add(business)
    await db.commit()
    await db.refresh(business)

    token = create_access_token(str(business.id))
    return TokenResponse(
        access_token=token,
        business_id=str(business.id),
        name=business.name,
        email=business.email,
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.email == req.email))
    business = result.scalar_one_or_none()
    if not business or not verify_password(req.password, business.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(business.id))
    return TokenResponse(
        access_token=token,
        business_id=str(business.id),
        name=business.name,
        email=business.email,
    )


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Generate a password reset token. In production, send this via email."""
    result = await db.execute(select(Business).where(Business.email == req.email))
    business = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    if not business:
        return {"message": "If an account exists, a reset link has been sent"}

    reset_token = create_reset_token(req.email)

    # TODO: Send email with reset link containing the token
    # For now, log it (remove in production)
    print(f"[DEV] Password reset token for {req.email}: {reset_token}")

    return {"message": "If an account exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    email = decode_reset_token(req.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    result = await db.execute(select(Business).where(Business.email == email))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    business.password_hash = hash_password(req.new_password)
    await db.commit()

    return {"message": "Password reset successfully"}


@router.post("/change-password")
async def change_password(
    req: ChangePasswordRequest,
    business_id: str = Depends(get_current_business_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    if not verify_password(req.current_password, business.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    business.password_hash = hash_password(req.new_password)
    await db.commit()

    return {"message": "Password changed successfully"}


@router.get("/me")
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
