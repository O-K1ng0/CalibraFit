# 💪 CalibraFit — Virtual Personal Trainer

A full-stack fitness web application that generates **highly personalized 30-day workout plans** based on comprehensive user profiling — demographics, medical history, fitness experience, and available equipment.

## Tech Stack

| Layer      | Technology         | Purpose                                    |
|------------|--------------------|--------------------------------------------|
| Frontend   | Next.js + Tailwind | Interactive onboarding, dashboard, workout UI |
| Backend    | Python + FastAPI   | Workout engine, medical filtering, REST API |
| Database   | PostgreSQL         | Structured data, JSONB for flexible fields  |
| Animations | LottieFiles        | Exercise demonstrations                    |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+ (or SQLite for development)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # Edit with your DB credentials
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd app
npm install
cp .env.example .env.local   # Edit with your API URL
npm run dev
```

### Database Setup
```bash
psql -U your_user -d calibrafit -f database/schema.sql
```

## Architecture

```
CalibraFit/
├── app/          → Next.js frontend (App Router)
├── backend/      → FastAPI backend
│   ├── app/api/  → REST endpoints
│   ├── app/core/ → Workout generation engine
│   ├── app/db/   → ORM models & connection
│   └── app/schemas/ → Pydantic validation
└── database/     → SQL schema scripts
```

## Key Features

- 🏋️ **Personalized Plans** — 30-day workout plans tailored to your fitness level
- 🩺 **Medical Safety** — Smart engine filters unsafe exercises based on medical history
- 🎬 **Animated Demos** — Exercise demonstrations with Lottie animations
- 📊 **Progress Tracking** — Streak counters, completion logs, visual progress
- 🔒 **Secure** — JWT auth, encrypted medical data, HIPAA-aware design

## License

Private — All rights reserved.
