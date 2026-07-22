"""
CalibraFit — Workout Plan API Endpoints
Generate plans, fetch daily workouts, log completions, and track progress.
"""

from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db.models import User, WorkoutPlan, DailyWorkout, CompletedWorkout, WeeklyFeedback, UserProfile, MedicalHistory
from app.schemas.workout import (
    WorkoutPlanResponse, WorkoutPlanSummary,
    DailyWorkoutResponse, ExerciseInRoutine,
    WorkoutCompletionCreate, WorkoutCompletionResponse,
    ProgressResponse, GeneratePlanRequest,
    WeeklyFeedbackCreate, WeeklyFeedbackResponse,
)
from app.core.security import get_current_user
from app.core.workout_generator import generate_workout_plan

router = APIRouter(prefix="/api/workout", tags=["Workout Plans"])


# ─── Plan Generation ────────────────────────────────────────

@router.post("/generate-plan", response_model=WorkoutPlanSummary)
def generate_plan(
    request: GeneratePlanRequest = GeneratePlanRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a personalized workout plan for the authenticated user.
    This triggers the core workout generation engine.
    """
    try:
        plan = generate_workout_plan(
            db=db,
            user=current_user,
            start_date=request.start_date,
            duration_days=request.duration_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Build summary
    daily_workouts = db.query(DailyWorkout).filter(DailyWorkout.plan_id == plan.plan_id).all()
    workout_days = sum(1 for d in daily_workouts if d.day_type != "Rest")
    rest_days = sum(1 for d in daily_workouts if d.day_type == "Rest")

    return WorkoutPlanSummary(
        plan_id=plan.plan_id,
        user_id=plan.user_id,
        start_date=plan.start_date,
        end_date=plan.end_date,
        generated_at=plan.generated_at,
        total_days=len(daily_workouts),
        workout_days=workout_days,
        rest_days=rest_days,
    )


# ─── Plan Retrieval ─────────────────────────────────────────

@router.get("/plan", response_model=WorkoutPlanResponse)
def get_current_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the most recent workout plan for the authenticated user."""
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.user_id)
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workout plan found. Generate one first.",
        )

    # Load daily workouts
    daily_workouts = (
        db.query(DailyWorkout)
        .filter(DailyWorkout.plan_id == plan.plan_id)
        .order_by(DailyWorkout.date)
        .all()
    )

    # Build response with nested routines
    daily_responses = []
    for dw in daily_workouts:
        exercises = [ExerciseInRoutine(**ex) for ex in (dw.routine or [])]
        daily_responses.append(DailyWorkoutResponse(
            daily_workout_id=dw.daily_workout_id,
            plan_id=dw.plan_id,
            date=dw.date,
            day_type=dw.day_type,
            routine=exercises,
        ))

    return WorkoutPlanResponse(
        plan_id=plan.plan_id,
        user_id=plan.user_id,
        start_date=plan.start_date,
        end_date=plan.end_date,
        generated_at=plan.generated_at,
        daily_workouts=daily_responses,
    )


@router.get("/plan/summary", response_model=WorkoutPlanSummary)
def get_plan_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a summary of the current workout plan."""
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.user_id)
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No workout plan found.")

    daily_workouts = db.query(DailyWorkout).filter(DailyWorkout.plan_id == plan.plan_id).all()
    workout_days = sum(1 for d in daily_workouts if d.day_type != "Rest")
    rest_days = sum(1 for d in daily_workouts if d.day_type == "Rest")

    return WorkoutPlanSummary(
        plan_id=plan.plan_id,
        user_id=plan.user_id,
        start_date=plan.start_date,
        end_date=plan.end_date,
        generated_at=plan.generated_at,
        total_days=len(daily_workouts),
        workout_days=workout_days,
        rest_days=rest_days,
    )


# ─── Daily Workout ──────────────────────────────────────────

@router.get("/daily/{workout_date}", response_model=DailyWorkoutResponse)
def get_daily_workout(
    workout_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the workout for a specific date."""
    # Find the user's active plan that covers this date
    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.user_id == current_user.user_id,
            WorkoutPlan.start_date <= workout_date,
            WorkoutPlan.end_date >= workout_date,
        )
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No workout plan found covering {workout_date}",
        )

    daily = (
        db.query(DailyWorkout)
        .filter(
            DailyWorkout.plan_id == plan.plan_id,
            DailyWorkout.date == workout_date,
        )
        .first()
    )
    if not daily:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No workout found for {workout_date}",
        )

    exercises = [ExerciseInRoutine(**ex) for ex in (daily.routine or [])]
    return DailyWorkoutResponse(
        daily_workout_id=daily.daily_workout_id,
        plan_id=daily.plan_id,
        date=daily.date,
        day_type=daily.day_type,
        routine=exercises,
    )


# ─── Workout Completion ─────────────────────────────────────

@router.post("/complete", response_model=WorkoutCompletionResponse, status_code=status.HTTP_201_CREATED)
def complete_workout(
    completion_data: WorkoutCompletionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a completed workout."""
    # Verify the daily workout exists and belongs to user
    daily = db.query(DailyWorkout).filter(
        DailyWorkout.daily_workout_id == completion_data.daily_workout_id
    ).first()
    if not daily:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily workout not found")

    plan = db.query(WorkoutPlan).filter(WorkoutPlan.plan_id == daily.plan_id).first()
    if plan.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your workout")

    # Check for duplicate completion
    existing = db.query(CompletedWorkout).filter(
        CompletedWorkout.daily_workout_id == completion_data.daily_workout_id,
        CompletedWorkout.user_id == current_user.user_id,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Workout already completed")

    completion = CompletedWorkout(
        user_id=current_user.user_id,
        daily_workout_id=completion_data.daily_workout_id,
        sets_completed=[s.model_dump() for s in completion_data.sets_completed],
        reps_completed=[],
        duration_minutes=completion_data.duration_minutes,
        notes=completion_data.notes,
    )
    db.add(completion)
    db.commit()
    db.refresh(completion)

    return completion


# ─── Progress & Stats ───────────────────────────────────────

@router.get("/progress", response_model=ProgressResponse)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get workout progress and streak data for the authenticated user."""
    completions = (
        db.query(CompletedWorkout)
        .filter(CompletedWorkout.user_id == current_user.user_id)
        .order_by(CompletedWorkout.completed_at.desc())
        .all()
    )

    total = len(completions)

    # Calculate current streak
    current_streak = 0
    if completions:
        check_date = date.today()
        completed_dates = set()
        for c in completions:
            if c.completed_at:
                completed_dates.add(c.completed_at.date() if hasattr(c.completed_at, 'date') else c.completed_at)

        while check_date in completed_dates:
            current_streak += 1
            check_date -= timedelta(days=1)

        # If today isn't completed yet, check from yesterday
        if current_streak == 0:
            check_date = date.today() - timedelta(days=1)
            while check_date in completed_dates:
                current_streak += 1
                check_date -= timedelta(days=1)

    # Calculate longest streak
    longest_streak = 0
    if completions:
        completed_dates_sorted = sorted(set(
            c.completed_at.date() if hasattr(c.completed_at, 'date') else c.completed_at
            for c in completions if c.completed_at
        ))
        streak = 1
        for i in range(1, len(completed_dates_sorted)):
            if completed_dates_sorted[i] - completed_dates_sorted[i-1] == timedelta(days=1):
                streak += 1
            else:
                longest_streak = max(longest_streak, streak)
                streak = 1
        longest_streak = max(longest_streak, streak)

    # Workouts this week
    week_start = date.today() - timedelta(days=date.today().weekday())
    workouts_this_week = sum(
        1 for c in completions
        if c.completed_at and (c.completed_at.date() if hasattr(c.completed_at, 'date') else c.completed_at) >= week_start
    )

    # Completion rate (based on current plan)
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.user_id)
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )
    completion_rate = 0.0
    if plan:
        total_workout_days = db.query(DailyWorkout).filter(
            DailyWorkout.plan_id == plan.plan_id,
            DailyWorkout.day_type != "Rest",
            DailyWorkout.date <= date.today(),
        ).count()
        if total_workout_days > 0:
            completion_rate = round(total / total_workout_days * 100, 1)

    recent = completions[:5]

    return ProgressResponse(
        total_workouts_completed=total,
        current_streak=current_streak,
        longest_streak=longest_streak,
        workouts_this_week=workouts_this_week,
        completion_rate=min(completion_rate, 100.0),
        recent_completions=[WorkoutCompletionResponse.model_validate(c) for c in recent],
    )


# ─── Weekly Feedback ────────────────────────────────────────

@router.post("/feedback", response_model=WeeklyFeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    feedback: WeeklyFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit weekly check-in feedback."""
    # Prevent duplicate feedback for the same week and plan
    existing = db.query(WeeklyFeedback).filter(
        WeeklyFeedback.user_id == current_user.user_id,
        WeeklyFeedback.week_number == feedback.week_number,
        WeeklyFeedback.plan_id == feedback.plan_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feedback for week {feedback.week_number} already submitted."
        )

    fb = WeeklyFeedback(
        user_id=current_user.user_id,
        plan_id=feedback.plan_id,
        week_number=feedback.week_number,
        difficulty_rating=feedback.difficulty_rating,
        energy_level=feedback.energy_level,
        pros=feedback.pros,
        cons=feedback.cons,
        new_pain_areas=feedback.new_pain_areas,
        overall_satisfaction=feedback.overall_satisfaction,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


@router.get("/feedback", response_model=list[WeeklyFeedbackResponse])
def get_feedbacks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all weekly feedbacks for the current user's latest plan."""
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.user_id)
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )
    if not plan:
        return []

    feedbacks = (
        db.query(WeeklyFeedback)
        .filter(
            WeeklyFeedback.user_id == current_user.user_id,
            WeeklyFeedback.plan_id == plan.plan_id,
        )
        .order_by(WeeklyFeedback.week_number)
        .all()
    )
    return [WeeklyFeedbackResponse.model_validate(f) for f in feedbacks]


@router.post("/adaptive-regenerate", response_model=WorkoutPlanSummary)
def adaptive_regenerate(
    request: GeneratePlanRequest = GeneratePlanRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Regenerate a plan using weekly feedback to adapt difficulty.
    Analyzes all feedback from the previous plan:
      - If avg difficulty_rating < 1.5 → upgrade fitness level
      - If avg difficulty_rating > 2.5 → downgrade fitness level
      - If new_pain_areas reported → add contraindication flags
    """
    # Get latest plan's feedbacks
    latest_plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.user_id)
        .order_by(WorkoutPlan.generated_at.desc())
        .first()
    )

    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    medical = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first() if profile else None

    if latest_plan and profile:
        feedbacks = (
            db.query(WeeklyFeedback)
            .filter(
                WeeklyFeedback.user_id == current_user.user_id,
                WeeklyFeedback.plan_id == latest_plan.plan_id,
            ).all()
        )

        if feedbacks:
            avg_difficulty = sum(f.difficulty_rating for f in feedbacks) / len(feedbacks)
            levels = ["beginner", "moderate", "expert"]
            current_idx = levels.index(profile.fitness_experience or "beginner")

            # Adapt difficulty level
            if avg_difficulty < 1.5 and current_idx < 2:
                profile.fitness_experience = levels[current_idx + 1]
            elif avg_difficulty > 2.5 and current_idx > 0:
                profile.fitness_experience = levels[current_idx - 1]

            # Collect new pain areas from feedback and add to medical contraindications
            if medical:
                pain_map = {
                    "knees": "knee_injury", "knee": "knee_injury",
                    "shoulders": "shoulder_injury", "shoulder": "shoulder_injury",
                    "back": "lower_back_pain", "lower back": "lower_back_pain",
                    "wrists": "wrist_injury", "wrist": "wrist_injury",
                    "hips": "hip_replacement", "hip": "hip_replacement",
                    "neck": "neck_issues",
                    "ankles": "ankle_injury", "ankle": "ankle_injury",
                }
                existing_flags = set(medical.contraindication_flags or [])
                for f in feedbacks:
                    for area in (f.new_pain_areas or []):
                        flag = pain_map.get(area.lower())
                        if flag:
                            existing_flags.add(flag)
                    # Also parse the cons text for pain keywords
                    if f.cons:
                        cons_lower = f.cons.lower()
                        for keyword, flag in pain_map.items():
                            if keyword in cons_lower:
                                existing_flags.add(flag)
                medical.contraindication_flags = list(existing_flags)

            db.commit()

    # Now generate the new plan with the adapted profile
    try:
        plan = generate_workout_plan(
            db=db,
            user=current_user,
            start_date=request.start_date,
            duration_days=request.duration_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    daily_workouts = db.query(DailyWorkout).filter(DailyWorkout.plan_id == plan.plan_id).all()
    workout_days = sum(1 for d in daily_workouts if d.day_type != "Rest")
    rest_days = sum(1 for d in daily_workouts if d.day_type == "Rest")

    return WorkoutPlanSummary(
        plan_id=plan.plan_id,
        user_id=plan.user_id,
        start_date=plan.start_date,
        end_date=plan.end_date,
        generated_at=plan.generated_at,
        total_days=len(daily_workouts),
        workout_days=workout_days,
        rest_days=rest_days,
    )
