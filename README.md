# Guest Post & Backlink Management Engine

Ek complete full-stack project — Client & Order Management, Automated Link
Health Checker, Website Metrics Logger (DA/DR), Revenue & Earnings
Analytics, aur ek Real-Time Dashboard. Login page se dashboard tak, sab
kuch professionally styled.

## Folder Structure

```
guest-post-engine/
├── backend/                     ← Python (FastAPI) — Clean Architecture
│   ├── app/
│   │   ├── domain/              ← Entities + Repository interfaces (pure business rules)
│   │   ├── application/         ← Services (use-cases) — ClientService, OrderService,
│   │   │                          LinkCheckerService, WebsiteService, AnalyticsService, AuthService
│   │   ├── infrastructure/      ← SQLAlchemy models, DB repos, HTTP link-checker, security (JWT/bcrypt)
│   │   ├── presentation/        ← FastAPI routes + Pydantic schemas + DI wiring (deps.py)
│   │   ├── core/                ← config.py, security.py
│   │   └── main.py              ← app entrypoint (also serves the frontend)
│   ├── seed.py                  ← creates the default admin login
│   ├── requirements.txt
│   └── .env.example             ← copy this to `.env` and fill in your DB details
└── frontend/                    ← Plain HTML/CSS/JS (no build step needed)
    ├── index.html               ← Login page
    ├── dashboard.html           ← Main dashboard (tabs: Overview, Clients, Websites, Orders, Analytics)
    ├── css/style.css
    └── js/ (api.js, auth.js, dashboard.js)
```

## Kaise Chalayen (Setup — step by step)

### 1. Python install karein (agar nahi hai)
Python 3.10+ chahiye.

### 2. Backend folder mein jayein aur dependencies install karein
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows par: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database set karein
`.env.example` ko `.env` mein copy karein:
```bash
cp .env.example .env
```
Phir `.env` file kholein aur `DATABASE_URL` update karein apni PostgreSQL details ke sath:
```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/guest_post_engine
```
**Note:** Agar aap abhi PostgreSQL install nahi karna chahte, `.env` mein `DATABASE_URL` line ko
delete/comment kar dein — project automatically ek local SQLite file (`guest_post_engine.db`)
use kar lega, taake aap turant test kar sakein. Baad mein jab PostgreSQL ready ho, bas
`.env` mein URL daal dein — code mein kuch change nahi karna padega.

PostgreSQL use kar rahe hain to database pehle create karein:
```sql
CREATE DATABASE guest_post_engine;
```

### 4. Tables banayein aur admin login create karein
```bash
python seed.py
```
Ye output dega: `Created admin user: admin / admin123`

### 5. Server start karein
```bash
uvicorn app.main:app --reload
```

### 6. Browser mein kholein
```
http://localhost:8000
```
Login page khulega → `admin` / `admin123` se login karein → phir professional
dashboard khulega (sidebar + tabs, sab kuch real-time, bina page reload ke).

## Important
- Login username/password `.env` mein `DEFAULT_ADMIN_USERNAME` / `DEFAULT_ADMIN_PASSWORD`
  se change kar sakte hain (seed.py chalane se pehle).
- Production mein `.env` ka `SECRET_KEY` zaroor change karein.
- API docs automatically yahan milenge: `http://localhost:8000/docs`
