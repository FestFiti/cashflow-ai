import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.models import Business, Invoice, Payment, Reminder, Notification, User, Service, InvoiceItem  # noqa: F401
from app.models.session import Session  # noqa - needed for create_all
from app.routers import auth, invoices, payments, webhooks, reminders, ai, dashboard, notifications, team, ws
from app.routers import profile, services


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="CashFlow AI",
    description="Intelligent Business Payment Orchestration API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for logos and other uploads
static_dir = os.path.join(os.path.dirname(__file__), "..", "static", "logos")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(team.router, prefix="/team", tags=["Team"])
app.include_router(ws.router, tags=["WebSocket"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(services.router, prefix="/services", tags=["Services"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "cashflow-ai"}
