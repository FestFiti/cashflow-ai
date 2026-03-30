# CashFlow AI — Pitch

## The Problem

African SMEs are bleeding money they've already earned.

- **60%** of businesses wait 45-60 days for payments
- **70%** still invoice manually — burning 15-20 hours per week
- **8-12%** of annual revenue is lost to payment delays alone
- **40%** cannot grow because cash is stuck in receivables

Kenya alone has 1.5 million registered SMEs. Most of them use WhatsApp, paper receipts, and Excel sheets to manage their cash flow. They send invoices, then spend weeks chasing payments — calling, texting, hoping.

There is no affordable, integrated tool built for how African businesses actually collect money: **M-Pesa**.

---

## The Solution

**CashFlow AI** is an intelligent payment orchestration platform that automates the entire cash flow cycle — from invoice creation to payment collection to reconciliation.

One sentence: **"Describe what you sold, we handle the rest."**

### How it works (live demo flow):

**Step 1 — Create an invoice in plain English**
> "Invoice John Kamau for 3 hours of web design at 5,000 per hour, due in 2 weeks"

Our AI parses this into a professional invoice with line items, calculates totals, and sets the due date. No forms. No templates. Just describe the transaction.

**Step 2 — Send and collect**
The invoice is emailed to your client with a shareable payment link. The client opens the link, taps "Pay", and receives an M-Pesa STK push on their phone. They enter their PIN. Done.

**Step 3 — Real-time tracking**
The moment payment lands, your dashboard updates via WebSocket. The invoice is marked paid. A receipt is emailed to your client. A notification appears in your app. Zero manual reconciliation.

**Step 4 — AI keeps you ahead**
If a payment is late, AI drafts a personalized reminder and sends it at the right time. Your dashboard shows aging analysis, collection rates, and cash flow forecasts — so you see problems before they happen.

---

## What We Built

### Core Platform
| Feature | What it does |
|---------|-------------|
| **AI Invoice Generator** | Natural language to professional invoices with line items |
| **M-Pesa STK Push** | One-tap payment collection via Safaricom Daraja API |
| **Public Payment Links** | Shareable URLs — clients pay without creating an account |
| **Real-Time Dashboard** | WebSocket-powered live updates on payments and cash flow |
| **AI Cash Flow Insights** | Actionable recommendations based on your financial data |
| **Smart Reminders** | AI-drafted payment reminders sent at optimal timing |
| **Reports & Analytics** | Revenue trends, aging analysis, top clients, collection rates |
| **Service Catalog** | Reusable services with pricing for faster invoice creation |
| **Team Management** | Multi-user access with role-based permissions |
| **Session Security** | Device tracking, IP logging, session revocation |
| **Branded Emails** | Welcome, login alerts, invoice notifications, payment receipts |

### Technical Architecture
```
SvelteKit (Frontend) → NGINX → FastAPI (Backend) → PostgreSQL + Redis
                                    ↓
                          M-Pesa / AI / eSMS Mail / Ratiba
```

- **Frontend**: SvelteKit 5 + TypeScript + TailwindCSS
- **Backend**: Python 3.12 / FastAPI (fully async)
- **Database**: PostgreSQL (asyncpg) + Redis (caching, M-Pesa token storage)
- **AI**: Claude API for invoice parsing, reminders, and insights
- **Payments**: M-Pesa Daraja API (STK Push, callbacks, OAuth token caching)
- **Email**: eSMS Mail API (transactional email delivery)
- **Deployment**: Docker Compose, GitHub Actions CI/CD

---

## Live Demo

**URL**: https://flowai.cash

### Demo Script (3 minutes)

1. **Login** — show the dashboard with real-time KPIs (receivables, collected, overdue)
2. **Create invoice** — type a natural language description, watch AI parse it into a structured invoice with line items
3. **Send invoice** — click send, show the branded email the client receives
4. **Payment link** — open the public payment URL, show the client-facing pay page
5. **M-Pesa STK Push** — initiate payment, show the phone prompt
6. **Real-time update** — dashboard updates instantly via WebSocket, invoice marked paid
7. **Reports** — show revenue chart, aging analysis, top clients
8. **AI Insights** — show the AI-generated cash flow recommendations
9. **WhatsApp share** — share invoice directly to client's WhatsApp with payment link

---

## Market Opportunity

| Metric | Value |
|--------|-------|
| Kenya SMEs | 1.5 million registered |
| East Africa (secondary) | Tanzania, Uganda, Rwanda |
| M-Pesa transactions (Kenya) | KES 35 trillion/year |
| Market size (Kenya) | $2.3 billion annually |
| Regional opportunity | $8.7 billion |

**Why now**: M-Pesa API (Daraja) is mature. AI costs are dropping. Smartphone penetration in Kenya is 60%+. SMEs are digitizing post-COVID.

---

## Business Model

**Freemium SaaS**:
- **Free tier**: 10 invoices/month, basic dashboard
- **Pro** (KES 1,500/month): Unlimited invoices, AI features, reports, team access
- **Business** (KES 5,000/month): API access, white-label, priority support

**Revenue streams**:
1. Monthly subscriptions
2. Transaction fees on M-Pesa collections (0.5% per transaction)
3. Premium AI features (forecasting, dispute resolution)

---

## Competitive Advantage

| Us | Them |
|----|------|
| M-Pesa native (STK Push built-in) | Most tools require manual payment entry |
| AI invoice generation (natural language) | Traditional form-based invoice creation |
| Real-time WebSocket updates | Refresh-to-check status |
| Built for African SMEs | Generic global tools adapted for Africa |
| Public payment links (no client signup) | Require both parties to have accounts |
| Integrated reminders + insights | Separate tools for each function |

---

## Traction / Validation

- Fully functional product deployed at flowai.cash
- End-to-end M-Pesa payment flow working (sandbox)
- AI invoice generation parsing natural language accurately
- Real-time dashboard with WebSocket updates
- Complete reports suite (6 API endpoints, visual charts)
- Email delivery system operational (eSMS Mail)
- 10 database tables, 14 API routers, 24 frontend routes

---

## The Team — Gatekeepers Group

| Name | Role | Contribution |
|------|------|-------------|
| **Beth Kimani** | AI/ML Engineer | Claude integration, NLP invoice parsing, cash flow forecasting |
| **Oliver Jackson** | Cyber Security | Authentication, encryption, session management, compliance |
| **Osborne Nyakaru** | AI/ML Engineer | Invoice generation models, anomaly detection, AI insights |
| **Stanley Onyango** | Software Engineer | FastAPI backend, M-Pesa integration, database architecture |
| **Steve Tom** | Software Developer | SvelteKit frontend, UI/UX design, real-time dashboard |

---

## The Ask

We're looking for:
1. **Mentorship** — connections to M-Pesa ecosystem partners and SME networks
2. **Pilot customers** — 50 Kenyan SMEs for a 3-month beta program
3. **Seed funding** — to scale infrastructure, hire, and expand to Tanzania/Uganda

---

## One-Liner

**CashFlow AI turns "Where's my money?" into "Your money is here."**

We help African businesses get paid faster by combining AI-powered invoicing with M-Pesa payment collection — so they can stop chasing payments and start growing.

---

*Built by Gatekeepers Group*
