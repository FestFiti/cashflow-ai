"""
Demo seed script — creates realistic demo data for CashFlow AI presentation.
Usage:
    python seed_demo.py [--email demo@flowai.cash] [--password Demo1234!]

Creates (or reuses) a demo business account, then inserts a mix of invoices,
payments, and notifications that make the dashboard look active.
"""
import argparse
import asyncio
import random
import uuid
from datetime import date, datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.business import Business
from app.models.invoice import Invoice
from app.models.notification import Notification
from app.models.payment import Payment
from app.models import *  # noqa: F401,F403 — ensure all models are registered

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------------------------------------------------------
# Demo dataset
# ---------------------------------------------------------------------------

CLIENTS = [
    {"name": "Wanjiku Mwangi",  "phone": "254712345601", "email": "wanjiku@nexatech.co.ke"},
    {"name": "Brian Otieno",    "phone": "254722345602", "email": "brian@buildkenya.co.ke"},
    {"name": "Amina Hassan",    "phone": "254733345603", "email": "amina@sahara-imports.com"},
    {"name": "David Kimani",    "phone": "254710345604", "email": None},
    {"name": "Grace Njeri",     "phone": "254742345605", "email": "grace@bloombrand.ke"},
    {"name": "Kevin Odhiambo",  "phone": "254753345606", "email": None},
    {"name": "Fatuma Ali",      "phone": "254764345607", "email": "fatuma@eastcoastlogistics.co.ke"},
    {"name": "James Mutua",     "phone": "254775345608", "email": "james@mutua-consulting.com"},
    {"name": "Cynthia Karanja", "phone": "254786345609", "email": None},
    {"name": "Samuel Kipchoge", "phone": "254797345610", "email": "samuel@kip-enterprises.co.ke"},
]

SERVICES = [
    ("Brand identity design & logo",       15000),
    ("Monthly social media management",     8500),
    ("Website redesign — 5 pages",         45000),
    ("SEO audit & content strategy",        12000),
    ("Product photography (30 shots)",      18000),
    ("Company brochure printing (500pcs)",  22000),
    ("Mobile app UI/UX design",             60000),
    ("Google Ads campaign setup",            9500),
    ("Annual bookkeeping services",         35000),
    ("Staff training — digital tools",      14000),
]

RECEIPTS = [
    "RAB12C3D4E", "SBK39F2G7H", "QMP44H8J2K", "LNR21A5B9C",
    "TXV78D1E3F", "WYZ93G6H0I", "NKT55J4K7L", "PLQ66M2N8O",
]


def random_past_date(days_ago_min: int, days_ago_max: int) -> date:
    offset = random.randint(days_ago_min, days_ago_max)
    return (datetime.utcnow() - timedelta(days=offset)).date()


def random_future_date(days_ahead_min: int, days_ahead_max: int) -> date:
    offset = random.randint(days_ahead_min, days_ahead_max)
    return (datetime.utcnow() + timedelta(days=offset)).date()


async def seed(email: str, password: str) -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # ------------------------------------------------------------------
        # 1. Upsert demo business
        # ------------------------------------------------------------------
        result = await db.execute(select(Business).where(Business.email == email))
        business = result.scalar_one_or_none()

        if business is None:
            business = Business(
                id=uuid.uuid4(),
                name="Fifi Creative Studio",
                email=email,
                phone="254700000000",
                password_hash=pwd_ctx.hash(password),
            )
            db.add(business)
            await db.flush()
            print(f"Created business: {business.name} ({email})")
        else:
            print(f"Reusing existing business: {business.name} ({email})")

        bid = business.id

        # ------------------------------------------------------------------
        # 2. Clear existing demo invoices / payments / notifications
        # ------------------------------------------------------------------
        existing = (await db.execute(
            select(Invoice).where(Invoice.business_id == bid)
        )).scalars().all()
        for inv in existing:
            for pay in inv.payments:
                await db.delete(pay)
            await db.delete(inv)

        existing_notifs = (await db.execute(
            select(Notification).where(Notification.business_id == bid)
        )).scalars().all()
        for n in existing_notifs:
            await db.delete(n)

        await db.flush()

        # ------------------------------------------------------------------
        # 3. Seed invoices
        # ------------------------------------------------------------------
        invoices_data = [
            # (client_idx, service_idx, status, amount_override, days_ago_created, due_offset)
            (0, 6, "paid",    None,  30,  14),   # Wanjiku — web app design, paid
            (1, 0, "paid",    None,  25,  10),   # Brian — branding, paid
            (2, 4, "paid",    None,  20,   7),   # Amina — photography, paid
            (3, 1, "paid",    None,  18,   5),   # David — social media, paid
            (4, 8, "sent",    None,   8,   7),   # Grace — bookkeeping, awaiting payment
            (5, 3, "sent",    None,   5,  10),   # Kevin — SEO audit, awaiting
            (6, 5, "overdue", None,  35, -10),   # Fatuma — brochure, overdue
            (7, 9, "overdue", None,  40,  -5),   # James — training, overdue
            (8, 7, "sent",    None,   2,  14),   # Cynthia — Google Ads, just sent
            (9, 2, "draft",   None,   0,  21),   # Samuel — website redesign, draft
        ]

        created_invoices: list[Invoice] = []
        receipt_pool = list(RECEIPTS)
        random.shuffle(receipt_pool)

        for c_idx, s_idx, status, amount_override, days_created, due_offset in invoices_data:
            client = CLIENTS[c_idx]
            service_desc, base_amount = SERVICES[s_idx]
            amount = amount_override or base_amount

            created_date = datetime.utcnow() - timedelta(days=days_created)
            due = date.today() + timedelta(days=due_offset)

            inv = Invoice(
                id=uuid.uuid4(),
                business_id=bid,
                client_name=client["name"],
                client_phone=client["phone"],
                client_email=client["email"],
                amount=amount,
                description=service_desc,
                due_date=due,
                status=status,
                created_at=created_date,
            )
            db.add(inv)
            created_invoices.append(inv)

        await db.flush()

        # ------------------------------------------------------------------
        # 4. Seed payments for paid invoices
        # ------------------------------------------------------------------
        for inv in created_invoices:
            if inv.status == "paid":
                paid_at = inv.created_at + timedelta(days=random.randint(1, 5))
                receipt = receipt_pool.pop() if receipt_pool else f"SIM{random.randint(10000,99999)}"
                pay = Payment(
                    id=uuid.uuid4(),
                    invoice_id=inv.id,
                    checkout_request_id=None,
                    mpesa_receipt=receipt,
                    amount=inv.amount,
                    phone=inv.client_phone,
                    status="completed",
                    paid_at=paid_at,
                    created_at=paid_at,
                )
                db.add(pay)

        await db.flush()

        # ------------------------------------------------------------------
        # 5. Seed notifications
        # ------------------------------------------------------------------
        now = datetime.utcnow()
        notifications = [
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Payment received",
                message="Wanjiku Mwangi paid KES 60,000 — receipt RAB12C3D4E",
                category="payment", is_read=True, created_at=now - timedelta(days=28),
                link=f"/invoices/{created_invoices[0].id}",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Payment received",
                message="Brian Otieno paid KES 15,000 — receipt SBK39F2G7H",
                category="payment", is_read=True, created_at=now - timedelta(days=23),
                link=f"/invoices/{created_invoices[1].id}",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Payment received",
                message="Amina Hassan paid KES 18,000 — receipt QMP44H8J2K",
                category="payment", is_read=False, created_at=now - timedelta(days=18),
                link=f"/invoices/{created_invoices[2].id}",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Invoice overdue",
                message="Fatuma Ali — KES 22,000 for brochure printing is 10 days overdue",
                category="alert", is_read=False, created_at=now - timedelta(days=10),
                link=f"/invoices/{created_invoices[6].id}",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Invoice overdue",
                message="James Mutua — KES 14,000 for staff training is 5 days overdue",
                category="alert", is_read=False, created_at=now - timedelta(days=5),
                link=f"/invoices/{created_invoices[7].id}",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="AI Insight ready",
                message="Your collection rate improved 12% this month. 2 clients need follow-up.",
                category="ai", is_read=False, created_at=now - timedelta(hours=3),
                link="/dashboard",
            ),
            Notification(
                id=uuid.uuid4(), business_id=bid,
                title="Payment received",
                message="David Kimani paid KES 8,500 — receipt LNR21A5B9C",
                category="payment", is_read=False, created_at=now - timedelta(hours=1),
                link=f"/invoices/{created_invoices[3].id}",
            ),
        ]
        for n in notifications:
            db.add(n)

        await db.commit()

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        paid = [i for i in created_invoices if i.status == "paid"]
        sent = [i for i in created_invoices if i.status == "sent"]
        overdue = [i for i in created_invoices if i.status == "overdue"]
        draft = [i for i in created_invoices if i.status == "draft"]

        total_collected = sum(i.amount for i in paid)
        total_pending = sum(i.amount for i in sent)
        total_overdue = sum(i.amount for i in overdue)

        print(f"\n{'='*50}")
        print(f"  Demo seed complete!")
        print(f"{'='*50}")
        print(f"  Invoices : {len(created_invoices)}")
        print(f"    Paid   : {len(paid)}  (KES {total_collected:,.0f})")
        print(f"    Sent   : {len(sent)}  (KES {total_pending:,.0f})")
        print(f"    Overdue: {len(overdue)}  (KES {total_overdue:,.0f})")
        print(f"    Draft  : {len(draft)}")
        print(f"  Payments : {len(paid)} M-Pesa receipts")
        print(f"  Notifs   : {len(notifications)}")
        print(f"\n  Login → {email} / {password}")
        print(f"{'='*50}\n")

    await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed demo data for CashFlow AI")
    parser.add_argument("--email",    default="demo@flowai.cash",  help="Demo account email")
    parser.add_argument("--password", default="Demo1234!",          help="Demo account password")
    args = parser.parse_args()
    asyncio.run(seed(args.email, args.password))
