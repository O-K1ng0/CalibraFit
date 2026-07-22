"""
CalibraFit — FastAPI Application Entry Point
Configures the app, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import create_tables, SessionLocal
from app.db.models import Exercise
from app.api import auth, user, workout

# Import seed data (ensure it's in python path)
try:
    from seed_exercises import EXERCISES
except ImportError:
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from seed_exercises import EXERCISES

settings = get_settings()

# ─── Application Instance ───────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Virtual Personal Trainer — Personalized workout plan generation with medical safety filtering.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS Middleware ─────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # Keeps your local testing working
        "https://calibrafit.vercel.app" # Your live Next.js frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include Routers ─────────────────────────────────────────

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(workout.router)

# ─── Lifecycle Events ────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    """Create database tables on startup and seed if necessary."""
    if settings.DEBUG:
        create_tables()
        
    # Auto-seed the database if exercises table is empty
    with SessionLocal() as db:
        if db.query(Exercise).count() == 0:
            print("Exercises table is empty. Auto-seeding database...")
            for ex_data in EXERCISES:
                exercise = Exercise(**ex_data)
                db.add(exercise)
            try:
                db.commit()
                print(f"Successfully seeded {len(EXERCISES)} exercises.")
            except Exception as e:
                db.rollback()
                print(f"Error seeding database: {e}")


# ─── Health Check ────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
