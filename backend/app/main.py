"""
CalibraFit — FastAPI Application Entry Point
Configures the app, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import create_tables
from app.api import auth, user, workout

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
    allow_origins=settings.CORS_ORIGINS,
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
    """Create database tables on startup (development mode)."""
    if settings.DEBUG:
        create_tables()


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
