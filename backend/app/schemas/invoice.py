import uuid
from datetime import date, datetime
from pydantic import BaseModel


class InvoiceCreate(BaseModel):
    client_name: str
    client_phone: str
    client_email: str | None = None
    amount: float
    description: str
    due_date: date


class InvoiceUpdate(BaseModel):
    client_name: str | None = None
    client_phone: str | None = None
    client_email: str | None = None
    amount: float | None = None
    description: str | None = None
    due_date: date | None = None
    status: str | None = None


class InvoiceResponse(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    client_name: str
    client_phone: str
    client_email: str | None
    amount: float
    description: str
    due_date: date
    status: str
    payment_url: str | None
    pdf_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
