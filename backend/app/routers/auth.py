from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib
from datetime import datetime

from app.database import get_db
from app.models.business import Business
from app.models.session import Session
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
from app.services.email import send_email
from app.services.email_templates import welcome_email, password_reset_email, login_notification_email

router = APIRouter()


def parse_device(user_agent: str) -> str:
    ua = user_agent.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        device_type = "Mobile"
    else:
        device_type = "Desktop"

    if "chrome" in ua:
        browser = "Chrome"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "safari" in ua:
        browser = "Safari"
    elif "edge" in ua:
        browser = "Edge"
    else:
        browser = "Browser"

    if "windows" in ua:
        os_name = "Windows"
    elif "mac" in ua:
        os_name = "Mac"
    elif "linux" in ua:
        os_name = "Linux"
    elif "android" in ua:
        os_name = "Android"
    elif "ios" in ua or "iphone" in ua or "ipad" in ua:
        os_name = "iOS"
    else:
        os_name = "Unknown OS"

    return f"{browser} on {os_name} ({device_type})"


@router.post("/quick-login", response_model=TokenResponse)
async def quick_login(db: AsyncSession = Depends(get_db)):
    """Quick login with default credentials for demo purposes"""
    email = "test@example.com"
    password = "pass123"
    
    # Check if user exists, create if not
    result = await db.execute(select(Business).where(Business.email == email))
    business = result.scalar_one_or_none()
    
    if not business:
        # Create default user
        business = Business(
            name="Allen Groceries",
            email=email,
            phone="0711888821",
            password_hash=hash_password(password),
            mpesa_shortcode="174379"
        )
        db.add(business)
        await db.commit()
        await db.refresh(business)
    
    # Verify password and create token
    if verify_password(password, business.password_hash):
        token = create_access_token(str(business.id))
        return TokenResponse(
            access_token=token,
            business_id=str(business.id),
            name=business.name,
            email=business.email,
        )
    
    raise HTTPException(status_code=401, detail="Default user creation failed")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
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

    subject, html = welcome_email(business.name)
    background_tasks.add_task(send_email, business.email, business.name, subject, html)

    return TokenResponse(
        access_token=token,
        business_id=str(business.id),
        name=business.name,
        email=business.email,
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.email == req.email))
    business = result.scalar_one_or_none()
    if not business or not verify_password(req.password, business.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session
    ip = request.headers.get("X-Forwarded-For", request.client.host if request.client else "unknown").split(",")[0].strip()
    ua = request.headers.get("User-Agent", "")
    device = parse_device(ua)

    session = Session(
        business_id=business.id,
        token_hash="pending",  # will update after token creation
        ip_address=ip,
        user_agent=ua[:500],
        device_name=device,
    )
    db.add(session)
    await db.flush()  # get session.id

    token = create_access_token(str(business.id), session_id=str(session.id))
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    session.token_hash = token_hash
    await db.commit()

    # Send login notification email (non-blocking)
    from datetime import timezone
    login_time = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    subject, html = login_notification_email(business.name, ip, device, "", login_time)
    background_tasks.add_task(send_email, business.email, business.name, subject, html)

    return TokenResponse(
        access_token=token,
        business_id=str(business.id),
        name=business.name,
        email=business.email,
    )


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.email == req.email))
    business = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    if not business:
        return {"message": "If an account exists, a reset link has been sent"}

    reset_token = create_reset_token(req.email)

    from datetime import timezone
    requested_at = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    subject, html = password_reset_email(business.name, reset_token, requested_at)
    background_tasks.add_task(send_email, business.email, business.name, subject, html)

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
