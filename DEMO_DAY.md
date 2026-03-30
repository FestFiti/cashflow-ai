# CashFlow AI

### Money in Motion Demo Day — 31st March 2026
### Convent International Hotel, Nairobi

---

## Elevator Pitch (30 seconds)

> We help **African freelancers and small businesses** who struggle with **getting paid on time and knowing where their money is** by offering **an AI-powered invoicing platform with built-in M-Pesa payments** — which lets them **create invoices in plain English, collect money via STK Push, and see every shilling in real time**. Unlike **QuickBooks, Wave, or Stripe**, our solution **is built natively for M-Pesa — the way 96% of Kenyans actually pay**. So far, we've **built a fully working product with live M-Pesa payments, AI invoice generation, and real-time dashboards deployed at flowai.cash**. We're now **looking for 50 pilot SMEs and seed funding to scale across East Africa**.

---

## 1. Problem Risk — Is This Real?

Africa's freelancers and small businesses operate in a financial blind spot. This is not theoretical. It's quantifiable:

- **60%** of Kenyan SMEs wait **45-60 days** to get paid
- **70%** still invoice manually — burning **15-20 hours per week**
- **8-12%** of annual revenue is **lost** to payment delays
- **40%** cannot scale because cash is stuck in receivables
- **1.5 million** registered SMEs in Kenya. **7.4 million** informal workers.

**How do we know this?** Because we've lived it. Our team has worked with freelancers, small agencies, and informal traders across Nairobi. The pattern is always the same:

1. Send invoice (WhatsApp PDF or verbal agreement)
2. Wait. Chase. Call. Text. Hope.
3. Money arrives — eventually — with no record tying it to the original job
4. At month end, no one knows what's owed, what's paid, or what's overdue

There is no affordable, integrated tool built for how African businesses actually collect money: **M-Pesa**.

**The tools that exist don't fit.** QuickBooks, Wave, and Stripe were built for bank transfers and credit cards. They don't support M-Pesa STK Push. They don't understand that a Kenyan freelancer's client pays by entering a phone number and a PIN — not a card number.

---

## 2. Solution / Product Risk — Does It Work?

**Yes. It's live. You can test it right now: [flowai.cash](https://flowai.cash)**

CashFlow AI replaces the chaos with a single, intelligent workflow:

### Create (AI-Powered)

Describe what you sold in plain English:

> *"Invoice John Kamau for 3 hours of web design at 5,000 per hour, due in 2 weeks"*

AI parses this into a professional invoice with line items, calculated totals, and a due date. No forms. No templates. Or create manually with a full service catalog.

### Send (Multi-Channel)

Invoice delivered via branded email with a **public payment link**. No signup required from the client. One tap to share the same invoice on WhatsApp — pre-filled with client phone, amount, line items, and payment link.

### Pay (M-Pesa STK Push)

Client opens the link, enters phone number, taps "Pay". M-Pesa STK Push triggers instantly — payment prompt on their phone. They enter PIN. Done.

No bank details. No card numbers. No friction.

### Track (Real-Time)

The moment payment lands, the dashboard updates via WebSocket. Invoice marked paid. Receipt emailed to client. Notification in-app. Zero manual reconciliation.

### Understand (AI Insights)

AI-generated cash flow insights. Aging reports show which receivables are at risk. Revenue charts show 6-month trends. Top client analysis shows who pays on time and who doesn't.

**What makes the product defensible (our moat):**
- M-Pesa is deeply integrated — not bolted on. STK Push, OAuth caching, webhook callbacks, auto-reconciliation.
- AI invoice generation from natural language — no competitor in this market does this.
- Real-time WebSocket updates — not refresh-to-check.
- Public payment links — your client doesn't need an account or an app.

### Product Roadmap (we know what's next)

| Timeline | Milestone |
|----------|-----------|
| **Q2 2026** | Multi-currency (TZS, UGX), Tanzania/Uganda mobile money, PDF invoices, SMS reminders |
| **Q3 2026** | Credit scoring from payment history, cash flow forecasting, expense tracking, recurring invoices |
| **Q4 2026** | Public API, B2C disbursements, Chama/group management, KRA iTax export |
| **2027** | West Africa (Nigeria, Ghana), enterprise white-label, financial data marketplace |

---

## 3. Business Model & Scaling Risk — How Do You Make Money?

### Revenue Streams

**1. Transaction Fees** — 0.5-1% on each M-Pesa payment collected through the platform. This is the primary driver at scale.

**2. Subscription Tiers**

| Tier | Price | What You Get |
|------|-------|-------------|
| **Free** | KES 0/month | 10 invoices/month, basic dashboard, M-Pesa payments |
| **Pro** | KES 1,500/month | Unlimited invoices, AI features, reports, team access, branded emails |
| **Business** | KES 5,000/month | API access, white-label invoices, priority support, advanced analytics |

**3. Enterprise (Future)** — Custom deployments for SACCOs, MFIs, and banks.

### Why This Model Scales

- **Transaction fees grow with usage** — no sales effort needed once a business is active
- **Subscription tiers create predictable revenue** alongside variable transaction income
- **API-first architecture** means enterprise integrations don't require custom builds
- **Unit economics**: Average SME sends 20-50 invoices/month at KES 15,000-50,000 average. At 0.5% fee = KES 1,500-12,500/month per business, before subscription revenue.

### Why This Business Model?

Because African SMEs won't pay upfront for software they haven't tested. The freemium model removes adoption friction. Transaction fees align our revenue with their success — we make money when they make money.

---

## 4. Finances Risk — Do You Know Your Numbers?

### What We Need and What It Gets

| Investment | Use | Outcome |
|-----------|-----|---------|
| **KES 500K** | Infrastructure (servers, Daraja production, monitoring) | Handle 1,000+ concurrent businesses |
| **KES 800K** | Growth (50-business pilot, marketing, onboarding) | Validate retention, collect usage data |
| **KES 700K** | Team (dedicated growth lead, 6 months) | Build repeatable acquisition channel |
| **Total: KES 2M** | **12-month runway** | **500 active businesses, KES 200K+ MRR** |

### Path to Profitability

- **Month 1-3**: Pilot with 50 businesses (free tier), validate product-market fit
- **Month 4-6**: Convert 30% to Pro tier, begin transaction fee collection
- **Month 7-12**: Scale to 500 businesses, hit KES 200K MRR
- **Month 12+**: Unit economics positive. Transaction fees compound with usage growth.

We are not burning cash on user acquisition. Our product is the acquisition channel — a freelancer who gets paid faster tells other freelancers.

---

## 5. Market & Timing Risk — Is This Market Big Enough? Why Now?

### Total Addressable Market

| Market | Size | Opportunity |
|--------|------|-------------|
| **Kenya (primary)** | 1.5M registered SMEs + 7.4M informal workers | **$2.3 billion annually** |
| **East Africa** | Tanzania, Uganda, Rwanda | **$8.7 billion** |
| **Sub-Saharan Africa** | Nigeria, Ghana, South Africa | **$30+ billion** |

### Why Now — This Wasn't Possible 3 Years Ago

1. **Safaricom Daraja API is mature.** Developer self-service, reliable webhooks, sandbox + production. The M-Pesa integration layer we rely on simply wasn't stable enough before 2024.

2. **AI costs dropped 90%.** Natural language invoice generation is now viable at scale through API providers with free tiers and low-cost models. In 2022, this would have been prohibitively expensive.

3. **Smartphone penetration crossed 60% in Kenya.** A web-based platform now reaches the majority of SME owners — no native app download required.

4. **Post-COVID digitization.** SMEs that survived the pandemic are now actively seeking digital financial tools. The behavioural shift happened. The tools haven't caught up.

5. **Government push.** Kenya's government is actively promoting cashless transactions and digital record-keeping for tax compliance (KRA iTax). Businesses need tools that create audit trails.

### Market Growth Rate

M-Pesa transaction volume has grown **20%+ year-over-year** for the past 5 years. The SME digital tools market in Africa is projected to grow at **25% CAGR** through 2030. We are entering a market that is expanding, not contracting.

---

## 6. Team Risk — Why Us?

### Gatekeepers Group

| Name | Role | Why They Matter |
|------|------|----------------|
| **Steve Tom** | Lead Developer & Frontend | Built the entire SvelteKit frontend, real-time dashboard, and UI/UX. Full-stack builder who ships fast and iterates based on user feedback. |
| **Oliver Jackson** | Security & Infrastructure | Designed authentication, session management, encryption, and deployment. In a fintech product handling real money, security isn't optional — Oliver ensures we're built right. |
| **Njeri (Beth Kimani)** | AI & Product | Led AI integration — invoice parsing, reminder drafting, cash flow insights. The bridge between what AI can do and what users actually need. |
| **Stan Lee (Stanley Onyango)** | Backend & Payments | Built the FastAPI backend, M-Pesa Daraja integration, database architecture, and webhook processing. Every payment that flows through our system runs on his code. |
| **Osbon (Osborne Nyakaru)** | AI & Data | Co-developed AI models, anomaly detection, and reporting analytics. Turns raw transaction data into the insights that make our dashboard valuable. |

### Why This Team

- **We built a production-ready fintech product in a hackathon sprint.** End-to-end: AI, payments, real-time updates, branded emails, reports. That velocity doesn't stop after demo day.
- **Complementary skills.** Frontend, backend, AI, security, data. No single point of failure.
- **We understand the market.** We're not building from Silicon Valley. We're in Nairobi, and we've seen the problem firsthand.

---

## 7. Exit Risk — Are You Committed?

### Our Commitment

This is not a hackathon project we'll abandon on Monday. CashFlow AI addresses a **$2.3 billion market** with no dominant local player. We are committed to building this into a company.

### Exit Potential

The African fintech space has proven exit pathways:
- **Flutterwave** — $3B valuation (payments infrastructure, Africa)
- **Chipper Cash** — acquired by Stripe (cross-border payments, Africa)
- **Paystack** — acquired by Stripe for $200M (Nigeria payments)
- **DPO Group** — acquired by Network International for $288M (pan-African payments)

### What We Need to Achieve Before Thinking Exit

1. **10,000+ active businesses** processing payments monthly
2. **Multi-country presence** (Kenya, Tanzania, Uganda minimum)
3. **KES 5M+ MRR** from combined transaction fees and subscriptions
4. **API platform** being used by third-party integrators

At that point, we become an acquisition target for pan-African payment platforms, banks expanding their SME tooling, or global fintech companies entering the African market.

---

## Live Demo

**URL**: [flowai.cash](https://flowai.cash)

### What the Judges Will See

| Feature | What Happens |
|---------|-------------|
| **Login** | Dashboard with real-time KPIs — receivables, collected, overdue |
| **AI Invoice** | Type natural language, watch AI parse it into structured invoice with line items |
| **Send Invoice** | Branded email delivered to client inbox |
| **Payment Link** | Public URL — client pays without any account |
| **M-Pesa STK Push** | Payment prompt on client's phone, enter PIN, done |
| **Real-Time Update** | Dashboard updates instantly via WebSocket |
| **Reports** | Revenue chart, aging analysis, top clients, collection rate |
| **AI Insights** | Actionable cash flow recommendations rendered as formatted text |
| **WhatsApp Share** | Invoice shared directly to client's WhatsApp with full details |

**Technical scope**: 14 API routers, 10 database models, 24 frontend routes, 5 external API integrations, Docker deployment, CI/CD via GitHub Actions.

---

## The Ask

1. **50 pilot businesses** — 3-month beta to validate retention and transaction volume
2. **Safaricom ecosystem connections** — introductions to the Daraja partnerships team
3. **KES 2M seed funding** — 12-month runway to reach 500 active businesses and KES 200K MRR

---

## Closing

Every day, millions of African businesses send invoices into a void and hope the money comes back. They spend hours chasing payments instead of doing the work that earns them. They make decisions without data because they can't see their own cash flow.

CashFlow AI changes that. We give every freelancer and small business the same financial clarity that Fortune 500 companies have — powered by M-Pesa, driven by AI, and built from the ground up for how Africa does business.

The infrastructure is here. The market is ready. The product works.

**We're not pitching an idea. We're demonstrating a solution.**

---

*CashFlow AI — Built by Gatekeepers Group*
*Demo Day: 31st March 2026 | flowai.cash*
