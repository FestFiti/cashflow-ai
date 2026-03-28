import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class InviteUserRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    role: str = "viewer"  # owner, manager, accountant, viewer
    temporary_password: str


class UpdateRoleRequest(BaseModel):
    role: str  # manager, accountant, viewer


class UserResponse(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    email: str
    name: str
    role: str
    phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
