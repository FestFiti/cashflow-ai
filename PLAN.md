# CashFlow AI — Build Plan

## Phase 1: Foundation (Week 1)

### Goals
- Working auth flow (register/login with JWT)
- Manual invoice CRUD (no AI yet)
- Basic SvelteKit dashboard listing invoices
- Docker Compose running the full stack

### Tasks
- [ ] Set up FastAPI skeleton with CORS, health check, error handling
- [ ] Configure PostgreSQL with SQLAlchemy async + Alembic migrations
- [ ] Create database models: `businesses`, `invoices`, `payments`, `reminders`
- [ ] Implement JWT auth (register, login, token refresh)
- [ ] Build invoice CRUD routes (`POST`, `GET`, `PATCH`, `DELETE`)
- [ ] Scaffold SvelteKit app with TailwindCSS
- [ ] Build login/register pages
- [ ] Build dashboard page (invoice list, basic stats)
- [ ] Build invoice creation form (manual fields)
- [ ] Wire frontend API client with auth headers
- [ ] Docker Compose with PostgreSQL + Redis + backend + frontend

### Deliverable
A user can register, log in, create invoices manually, and see them on the dashboard.

---

## Phase 2: Payments (Week 2)

### Goals
- M-Pesa STK Push triggers from invoices
- Webhook receives payment confirmations
- Invoice status auto-updates on payment

### Tasks
- [ ] Implement Daraja API wrapper (`services/mpesa.py`)
  - OAuth token generation with Redis caching (55-min TTL)
  - STK Push (Lipa Na M-Pesa Online)
  - B2C disbursements
  - Transaction status queries
- [ ] Build payment routes (`POST /payments/stk-push`, `GET /payments/{id}/status`)
- [ ] Build webhook endpoints (`POST /webhooks/c2b`, `POST /webhooks/b2c-result`)
- [ ] Store `CheckoutRequestID` in Redis for callback matching
- [ ] Auto-flip invoice status to `PAID` on successful callback
- [ ] Add payment status component to frontend
- [ ] Add "Pay Now" button on invoice detail page
- [ ] Test end-to-end in Daraja sandbox

### Deliverable
A client receives an STK push on their phone, pays, and the invoice status updates in real time.

---

## Phase 3: AI Features (Week 3)

### Goals
- Claude-powered invoice generation from natural language
- AI-drafted reminder messages
- Cash flow insight summary on dashboard

### Tasks
- [ ] Implement Claude API wrapper (`services/claude.py`)
- [ ] Build AI invoice generation route
  - System prompt defining exact JSON schema
  - Parse natural language → structured invoice data
- [ ] Build AI reminder message drafting
  - Generate personalised SMS/email text per client context
- [ ] Build cash flow insight summary
  - Aggregate receivables/payables → send to Claude → return summary
- [ ] Add AI prompt bar component to frontend
- [ ] Add "Generate with AI" option to invoice creation
- [ ] Display AI insights on dashboard

### Deliverable
A user types "Invoice John Kamau KES 12,000 for web design, due April 5" and gets a complete invoice.

---

## Phase 4: Scheduling & Polish (Week 4)

### Goals
- Automated payment reminders via Ratiba
- B2C bulk payouts
- PDF invoice export
- Polished, production-ready UI

### Tasks
- [ ] Implement Ratiba API wrapper (`services/ratiba.py`)
- [ ] Auto-schedule reminders on invoice creation (7d, 1d, day-of, 1d overdue)
- [ ] Build reminder webhook endpoint (`POST /webhooks/ratiba`)
- [ ] Integrate Africa's Talking SMS for notifications
- [ ] Build PDF invoice generation with WeasyPrint + Jinja2 templates
- [ ] Add B2C bulk disbursement UI (pay workers/farmers)
- [ ] Build reports page (cash flow chart, client breakdown)
- [ ] Add dispute summariser (AI summarises payment conversation history)
- [ ] Add reconciliation bot (auto-match M-Pesa confirmations to invoices)
- [ ] UI polish: loading states, error handling, responsive design
- [ ] Write tests for critical paths

### Deliverable
Full working platform: AI invoicing → M-Pesa payment → automated reminders → real-time dashboard.

---

## Database Schema

```sql
-- Core tables
businesses    (id, name, email, phone, password_hash, mpesa_shortcode, created_at)
invoices      (id, business_id, client_name, client_phone, client_email,
               amount, description, due_date, status, payment_url, pdf_url, created_at)
payments      (id, invoice_id, checkout_request_id, mpesa_receipt,
               amount, phone, status, paid_at, created_at)
reminders     (id, invoice_id, ratiba_job_id, scheduled_at, message,
               status, sent_at, created_at)
```

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Async FastAPI + asyncpg | Handle concurrent M-Pesa webhooks without blocking |
| Redis for token/session caching | M-Pesa tokens expire hourly; avoid per-request auth |
| JWT in HttpOnly cookies | Secure auth that works with SvelteKit SSR |
| One `/dashboard/summary` endpoint | Avoid waterfall loading on the main page |
| Claude with structured JSON prompts | Reliable parsing without function calling overhead |
| Docker Compose for everything | One command to run the full stack locally |
