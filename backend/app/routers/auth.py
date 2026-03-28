from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.business import Business
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.utils.auth import hash_password, verify_password, create_access_token

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
    return TokenResponse(access_token=token, business_id=str(business.id), name=business.name)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).where(Business.email == req.email))
    business = result.scalar_one_or_none()
    if not business or not verify_password(req.password, business.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(business.id))
    return TokenResponse(access_token=token, business_id=str(business.id), name=business.name)
