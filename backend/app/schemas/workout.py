"""
CalibraFit — Workout Pydantic Schemas
Request/response validation models for workout plans, daily workouts, and completions.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


# ─── Exercise Detail in a Routine ────────────────────────────

class ExerciseInRoutine(BaseModel):
    exercise_id: int
    name: str
    description: Optional[str] = None
    target_muscle_primary: str
    target_muscle_secondary: list[str] = []
    equipment_required: list[str] = []
    difficulty: int = 1
    animation_url: Optional[str] = None
    sets: int = 3
    reps: int = 10
    rest_seconds: int = 60


# ─── Daily Workout ──────────────────────────────────────────

class DailyWorkoutResponse(BaseModel):
    daily_workout_id: int
    plan_id: int
    date: date
    day_type: Optional[str] = None
    routine: list[ExerciseInRoutine] = []

    model_config = {"from_attributes": True}


# ─── Workout Plan ───────────────────────────────────────────

class WorkoutPlanResponse(BaseModel):
    plan_id: int
    user_id: int
    start_date: date
    end_date: date
    generated_at: Optional[datetime] = None
    daily_workouts: list[DailyWorkoutResponse] = []

    model_config = {"from_attributes": True}


class WorkoutPlanSummary(BaseModel):
    plan_id: int
    user_id: int
    start_date: date
    end_date: date
    generated_at: Optional[datetime] = None
    total_days: int = 0
    workout_days: int = 0
    rest_days: int = 0

    model_config = {"from_attributes": True}


# ─── Completed Workout ──────────────────────────────────────

class SetCompletion(BaseModel):
    exercise_id: int
    set_number: int
    reps_done: int
    weight_used: Optional[float] = None


class WorkoutCompletionCreate(BaseModel):
    daily_workout_id: int
    sets_completed: list[SetCompletion] = Field(default_factory=list)
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None


class WorkoutCompletionResponse(BaseModel):
    completion_id: int
    user_id: int
    daily_workout_id: int
    completed_at: Optional[datetime] = None
    sets_completed: list[dict] = []
    reps_completed: list[dict] = []
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


# ─── Progress & Stats ───────────────────────────────────────

class ProgressResponse(BaseModel):
    total_workouts_completed: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    workouts_this_week: int = 0
    completion_rate: float = 0.0
    recent_completions: list[WorkoutCompletionResponse] = []


class GeneratePlanRequest(BaseModel):
    """Optional overrides when generating a new plan."""
    start_date: Optional[date] = None
    duration_days: int = Field(30, ge=7, le=90)


# ─── Weekly Feedback ────────────────────────────────────────

class WeeklyFeedbackCreate(BaseModel):
    """Submit weekly check-in feedback."""
    plan_id: Optional[int] = None
    week_number: int = Field(..., ge=1)
    difficulty_rating: int = Field(..., ge=1, le=3)  # 1=Too Easy, 2=Just Right, 3=Too Hard
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    pros: Optional[str] = None
    cons: Optional[str] = None
    new_pain_areas: list[str] = Field(default_factory=list)
    overall_satisfaction: Optional[int] = Field(None, ge=1, le=5)


class WeeklyFeedbackResponse(BaseModel):
    feedback_id: int
    user_id: int
    plan_id: Optional[int] = None
    week_number: int
    difficulty_rating: int
    energy_level: Optional[int] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    new_pain_areas: list[str] = []
    overall_satisfaction: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
