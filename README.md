# FinanceFlow

A personal finance tracking backend designed for clean architecture, demo-friendly access, and scalable SaaS features. Built with FastAPI and Firestore, FinanceFlow provides APIs for recording transactions, managing categories, and generating monthly financial summaries.

---

## Overview

FinanceFlow is the backend service for a personal finance web application.  
It enables users to manually track income and expenses, view monthly summaries, and explore the product instantly using a frictionless Demo Mode — all without creating an account.

This backend is designed with multi-tenant architecture from day one, supporting both demo users and future authenticated users.

---

## Features (MVP)

### ✔ Demo Mode (Instant Access)

- No signup required
- One button generates a temporary demo session
- Fully isolated demo user environment
- Safe to test all features without affecting others
- Data stored under `demo_users/{demo_id}`

### ✔ Categories (Income & Expense)

- Create, list, and delete categories
- Income categories (e.g., Salary)
- Expense categories (e.g., Rent, Groceries)

### ✔ Transactions

- Record income and expenses manually
- Fields include:
  - amount
  - type: INCOME / EXPENSE
  - category
  - date
  - description (optional)
- List transactions by month

### ✔ Monthly Reports (JSON)

- `/reports/monthly?year=YYYY&month=MM`
- Returns:
  - total income
  - total expenses
  - net savings
  - breakdown by category
  - daily spending timeline
- Frontend handles charts (no PDF in MVP)

---

## Architecture

FinanceFlow follows a clean, service-oriented backend structure using Firestore for storage and FastAPI for REST APIs.

```
Client (Frontend)
↓
[FastAPI Backend]
├─ Auth Middleware (Demo / User Mode)
├─ Services (Reports, Transactions, Categories)
├─ Repositories (Firestore)
└─ Models (Pydantic)
↓
Firestore
├─ demo_users/{demo_id}
└─ users/{uid} (future)
```

### Multi-Tenant Design

- Demo users → `demo_users/{demo_id}`
- Future real users → `users/{uid}`
- Shared business logic, isolated data paths

---

## Demo Mode

The backend offers an instant, passwordless demo experience.

### `POST /auth/demo`

Creates a temporary user with:

- `demo_id`
- Default categories
- Optional sample transactions
- A signed session token
- `expires_at` metadata

Demo users can:

- Add transactions
- Manage categories
- View monthly reports
- Use the full application experience

This allows new users or recruiters to explore FinanceFlow immediately.

---

## API Overview (MVP)

### Authentication

- `POST /auth/demo` — Create demo session

### Categories

- `GET /categories`
- `POST /categories`
- `DELETE /categories/{id}`

### Transactions

- `GET /transactions?year=YYYY&month=MM`
- `POST /transactions`

### Reports

- `GET /reports/monthly?year=YYYY&month=MM`

---

## Project Structure (Proposed)

```
FinanceFlow--BE/
├─ app.py                  # FastAPI entrypoint
├─ db/
│  └─ db_connector.py      # Firestore initialization + shared client
│
├─ src/
│  ├─ api/                 # Routers
│  │   ├─ auth.py
│  │   ├─ categories.py
│  │   ├─ transactions.py
│  │   └─ reports.py
│  │
│  ├─ services/            # Business logic
│  │   ├─ auth_service.py
│  │   ├─ category_service.py
│  │   ├─ transaction_service.py
│  │   └─ report_service.py
│  │
│  ├─ repos/               # Database access layer
│  │   ├─ category_repo.py
│  │   ├─ transaction_repo.py
│  │   └─ base_repo.py     # (optional shared repo utils)
│  │
│  ├─ models/              # Pydantic models (schemas)
│  │   ├─ transaction.py
│  │   ├─ category.py
│  │   └─ auth.py
│  │
│  ├─ core/                # Auth, config, middlewares, utils
│  │   ├─ config.py
│  │   ├─ auth.py          # JWT verification (demo mode)
│  │   └─ exceptions.py
│  │
│  └─ __init__.py
│
├─ requirements.txt
└─ README.md

```

## Roadmap

### MVP (In Progress)

- [ ] Demo Mode backend session
- [ ] Categories API
- [ ] Transactions API
- [ ] Monthly report service
- [ ] FastAPI skeleton + routers
- [ ] Firestore integration
- [ ] Basic frontend dashboard (separate repo)

### Phase 2

- [ ] Real user authentication (Firebase Auth)
- [ ] PDF report export (fpdf2)
- [ ] Receipt upload (optional)
- [ ] Settings (currency, timezone)
- [ ] Cron job for automated monthly summaries

### Phase 3

- [ ] Advanced analytics
- [ ] Budget goals + limits
- [ ] Import from CSV / bank exports
- [ ] Notifications

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** Firestore (NoSQL)
- **Auth:** JWT-based demo sessions (Firebase Auth for future users)
- **Deployment:** TBD (Cloud Run / Render / etc.)
- **Frontend:** Host separately (Netlify)

---

## License

© DreamRootLabs
