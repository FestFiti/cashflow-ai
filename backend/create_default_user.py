#!/usr/bin/env python3
"""Create default user for seamless login"""

import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.business import Business
from app.utils.auth import hash_password
from app.config import settings

# Database setup
engine = create_async_engine(settings.DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_default_user():
    """Create default user if it doesn't exist"""
    async with async_session() as db:
        # Check if user already exists
        result = await db.execute(
            select(Business).where(Business.email == "test@example.com")
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print("✅ Default user already exists")
            return existing
        
        # Create default user
        business = Business(
            name="Allen Groceries",
            email="test@example.com", 
            phone="0711888821",
            password_hash=hash_password("pass123"),
            mpesa_shortcode="174379"  # Default Daraja shortcode
        )
        
        db.add(business)
        await db.commit()
        await db.refresh(business)
        
        print(f"✅ Created default user: {business.name} ({business.email})")
        print(f"   Login: test@example.com / pass123")
        print(f"   User ID: {business.id}")
        
        return business

if __name__ == "__main__":
    asyncio.run(create_default_user())
