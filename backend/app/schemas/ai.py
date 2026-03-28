from pydantic import BaseModel


class AIInvoiceRequest(BaseModel):
    prompt: str


class AIInsightRequest(BaseModel):
    client_name: str | None = None
    amount: float | None = None
    due_date: str | None = None
    context: str | None = None
