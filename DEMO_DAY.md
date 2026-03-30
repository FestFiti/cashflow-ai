# CashFlow AI

### Money in Motion Demo Day — 31st March 2026
### Convent International Hotel, Nairobi

---

## Executive Summary

CashFlow AI is a financial management and payments platform built for freelancers and small businesses in Africa. It lets users create invoices — including through AI-assisted natural language — send them to clients, and collect payments instantly via M-Pesa. Every transaction is tracked in real time.

We exist because African freelancers and SMEs shouldn't need an accountant, a payment gateway, and three spreadsheets to know where their money is.

**Our vision**: Make financial management effortless for every business in Africa, starting with the 1.5 million SMEs in Kenya.

---

## The Problem

Africa's freelancers and small businesses operate in a financial blind spot.

**No visibility.** Most track payments through WhatsApp messages, notebooks, or memory. There is no single place to see what's owed, what's paid, and what's overdue.

**No structure.** Invoices are sent as PDFs over email — or not at all. There's no link between the invoice and the payment. Reconciliation is manual and error-prone.

**Delayed payments.** 60% of Kenyan SMEs wait 45-60 days to get paid. Without automated follow-ups, businesses lose time and revenue chasing clients.

**Trust gaps.** Clients dispute amounts. Freelancers can't prove what was agreed. There's no shared record that both parties can reference.

**Tools don't fit.** Global platforms like QuickBooks, Wave, and Stripe weren't built for M-Pesa. They don't support STK Push. They don't understand how African businesses actually collect money.

The result: **8-12% of annual revenue is lost to payment delays**, and 40% of SMEs cannot scale because cash is stuck in receivables.

---

## The Solution

CashFlow AI replaces the chaos with a single, intelligent workflow:

### Step 1 — Create

Describe what you sold in plain English:

> *"Invoice John Kamau for 3 hours of web design at 5,000 per hour, due in 2 weeks"*

Our AI parses this into a professional invoice with line items, calculated totals, and a due date. No forms. No templates. Alternatively, users can create invoices manually with a full service catalog.

### Step 2 — Send

The invoice is delivered to the client via email — branded with the business name and logo. It includes a **public payment link** that requires no signup or login from the client.

The same invoice can be shared directly via WhatsApp with a single tap — pre-filled with the client's phone number, amount, line items, and payment link.

### Step 3 — Pay

The client opens the payment link, enters their phone number, and taps "Pay". An **M-Pesa STK Push** is triggered instantly — a payment prompt appears on their phone. They enter their PIN. Payment complete.

No bank details. No card numbers. No friction.

### Step 4 — Track

The moment payment lands, the business owner's dashboard updates in real time via WebSocket. The invoice is marked as paid. A receipt is emailed to the client. A notification appears in the app.

Zero manual reconciliation.

### Step 5 — Understand

AI-generated cash flow insights tell you what to do next. Aging reports show which receivables are at risk. Revenue charts show trends over six months. Top client analysis reveals who pays on time and who doesn't.

You stop guessing and start making decisions based on data.

---

## M-Pesa Integration

M-Pesa is not an add-on. It is the foundation of our payment architecture.

**Why M-Pesa matters:**
- 96% of Kenyan adults use mobile money
- M-Pesa processes over KES 35 trillion annually
- It is the primary way SMEs and freelancers receive payments
- Global payment tools (Stripe, PayPal) don't operate natively in this ecosystem

**Our implementation:**

| Capability | Detail |
|-----------|--------|
| **STK Push** | Lipa Na M-Pesa Online — payment prompt sent directly to client's phone |
| **OAuth Token Caching** | M-Pesa access tokens cached in Redis with 55-minute TTL for performance |
| **Webhook Callbacks** | Real-time payment confirmation from Safaricom's Daraja API |
| **Auto-Reconciliation** | Payment receipt matched to invoice automatically — status updated, receipt emailed |
| **Phone Normalization** | Handles all Kenyan phone formats (0712..., +254712..., 254712...) |
| **Live Environment** | Production-ready Daraja integration, not sandbox |

When a client pays through CashFlow AI, the business knows within seconds. Not hours. Not days. Seconds.

---

## Competitive Advantage

| CashFlow AI | Traditional / Global Tools |
|-------------|---------------------------|
| M-Pesa STK Push built into the core | Require manual bank transfers or card payments |
| AI invoice generation from natural language | Form-based invoice creation |
| Public payment links — clients don't need accounts | Both parties must have accounts |
| Real-time WebSocket dashboard updates | Manual refresh to check status |
| Built for African payment behavior | Adapted (poorly) from US/EU workflows |
| Integrated reminders with AI-drafted messages | Separate tools for invoicing and communication |
| Branded emails + WhatsApp sharing | Basic email-only delivery |

**We are not adapting a Western tool for Africa. We built an African tool from day one.**

---

## Business Model

### Revenue Streams

**1. Transaction Fees**
0.5-1% fee on each M-Pesa payment collected through the platform. At scale, this is the primary revenue driver.

**2. Subscription Tiers**

| Tier | Price | Includes |
|------|-------|---------|
| **Free** | KES 0/month | 10 invoices/month, basic dashboard, M-Pesa payments |
| **Pro** | KES 1,500/month | Unlimited invoices, AI features, reports, team access, branded emails |
| **Business** | KES 5,000/month | API access, white-label invoices, priority support, advanced analytics |

**3. Enterprise (Future)**
Custom deployments for larger SMEs, SACCOs, and financial institutions. API-first architecture makes this possible from day one.

### Unit Economics
- Average SME sends 20-50 invoices/month
- Average invoice value: KES 15,000-50,000
- At 0.5% transaction fee: KES 1,500-12,500 revenue per active business per month
- Combined with subscription: strong LTV with low acquisition cost

---

## Market Opportunity

**Primary Market: Kenya**
- 1.5 million registered SMEs
- 7.4 million informal sector workers (many are freelancers)
- M-Pesa mobile money: 96% adult adoption
- Market size: **$2.3 billion annually** in invoicing and payment management

**Secondary Market: East Africa**
- Tanzania (M-Pesa, Tigo Pesa), Uganda (MTN Mobile Money), Rwanda (MTN MoMo)
- Combined opportunity: **$8.7 billion**

**Macro Trends:**
- Post-COVID digitization of SME operations
- Safaricom Daraja API maturity enabling developer integrations
- Growing freelancer economy (remote work, gig economy)
- Smartphone penetration in Kenya exceeding 60%
- Government push for cashless transactions and digital records

---

## Demo Readiness

This is not a prototype. This is a working product.

| What We'll Show | Status |
|----------------|--------|
| User registration and login | Live |
| AI-powered invoice creation (natural language) | Live |
| Manual invoice creation with line items | Live |
| Invoice delivery via email (branded) | Live |
| WhatsApp sharing with payment link | Live |
| Public payment page (no client login) | Live |
| M-Pesa STK Push payment | Live |
| Real-time dashboard update on payment | Live |
| Reports: revenue charts, aging, top clients | Live |
| AI cash flow insights | Live |
| Service catalog management | Live |
| Team management with roles | Live |
| Session security and device tracking | Live |
| Password reset with email delivery | Live |

**Live URL**: https://flowai.cash

**Technical scope**: 14 API endpoints, 10 database models, 24 frontend routes, 5 external API integrations, full Docker deployment.

---

## Future Roadmap

### Q2 2026 — Expansion
- **Multi-currency support** — USD, TZS, UGX alongside KES
- **Tanzania and Uganda** — integrate Tigo Pesa and MTN Mobile Money
- **PDF invoice generation** — downloadable, printable invoices with business branding
- **SMS reminders** — via Africa's Talking for clients without smartphones

### Q3 2026 — Intelligence
- **Credit scoring** — payment history analysis to assess client reliability
- **Cash flow forecasting** — AI-driven predictions of future cash position
- **Expense tracking** — complete picture of inflows and outflows
- **Recurring invoices** — automated monthly billing via Ratiba scheduling

### Q4 2026 — Platform
- **Public API** — let other platforms integrate CashFlow AI payments
- **B2C disbursements** — pay suppliers and contractors via M-Pesa
- **Chama/Group management** — contribution tracking for savings groups (Imarisha module)
- **Accounting integrations** — export to QuickBooks, Xero, KRA iTax

### 2027 — Scale
- **West Africa expansion** — Nigeria (Paystack), Ghana (MTN MoMo)
- **Enterprise tier** — white-label deployments for banks and MFIs
- **Financial insights marketplace** — anonymized data products for lenders

---

## The Team — Gatekeepers Group

We are five builders who understand both the technology and the market.

| Name | Role | What They Bring |
|------|------|----------------|
| **Steve Tom** | Lead Developer & Frontend | Built the entire SvelteKit frontend, real-time dashboard, and UI/UX. Owns the product experience. |
| **Oliver Jackson** | Security & Infrastructure | Designed authentication, session management, encryption, and deployment. Ensures the platform is secure and compliant. |
| **Njeri (Beth Kimani)** | AI & Product | Led Claude AI integration — invoice parsing, reminder drafting, cash flow insights. Bridges AI capability with user needs. |
| **Stan Lee (Stanley Onyango)** | Backend & Payments | Built the FastAPI backend, M-Pesa Daraja integration, database architecture, and webhook processing. The payment plumbing runs on his code. |
| **Osbon (Osborne Nyakaru)** | AI & Data | Co-developed AI models, anomaly detection, and reporting analytics. Turns raw transaction data into actionable intelligence. |

We built CashFlow AI in a hackathon sprint — and it works end-to-end with real payments. That should tell you something about what this team can do with more time and resources.

---

## The Ask

We are looking for:

1. **Pilot partners** — 50 Kenyan freelancers and SMEs for a 3-month beta to validate retention and transaction volume
2. **Strategic connections** — introductions to Safaricom's Daraja ecosystem team and SME networks
3. **Seed investment** — to scale infrastructure, expand to Tanzania/Uganda, and hire a dedicated growth lead

---

## Closing

Every day, millions of African businesses send invoices into a void and hope the money comes back. They spend hours chasing payments instead of doing the work that earns them. They make decisions without data because they can't see their own cash flow.

CashFlow AI changes that. We give every freelancer and small business the same financial clarity that Fortune 500 companies have — powered by M-Pesa, driven by AI, and built from the ground up for how Africa does business.

The infrastructure is here. The market is ready. The product works.

**We're not pitching an idea. We're demonstrating a solution.**

---

*CashFlow AI — Built by Gatekeepers Group*
*Demo Day: 31st March 2026 | flowai.cash*
