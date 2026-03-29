import uuid
from datetime import date, datetime
from pydantic import BaseModel


class InvoiceItemCreate(BaseModel):
    service_id: uuid.UUID | None = None
    name: str
    description: str | None = None
    quantity: int = 1
    unit_price: float


class InvoiceItemResponse(BaseModel):
    id: uuid.UUID
    invoice_id: uuid.UUID
    service_id: uuid.UUID | None
    name: str
    description: str | None
    quantity: int
    unit_price: float
    total: float

    model_config = {"from_attributes": True}


class InvoiceCreate(BaseModel):
    client_name: str
    client_phone: str
    client_email: str | None = None
    amount: float | None = None
    description: str
    due_date: date
    items: list[InvoiceItemCreate] | None = None


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
    items: list[InvoiceItemResponse] = []

    model_config = {"from_attributes": True}
