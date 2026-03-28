from pydantic import BaseModel


class AIInvoiceRequest(BaseModel):
    prompt: str


class AIInsightRequest(BaseModel):
    context: str | None = None
