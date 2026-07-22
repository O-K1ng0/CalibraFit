"""
CalibraFit — Core Workout Generation Engine

The heart of the application. Generates personalized 30-day workout plans by:
1. Fetching user profile and medical history
2. Filtering exercises by equipment, environment, and difficulty
3. Cross-referencing medical contraindications to exclude unsafe exercises
4. Finding safe alternatives for excluded exercises
5. Assembling a calendar-aware plan with proper muscle rotation
6. Scaling sets/reps based on fitness experience
"""

import random
from datetime import date, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.db.models import (
    User, UserProfile, MedicalHistory, Exercise,
    WorkoutPlan, DailyWorkout
)

# ─── Constants ───────────────────────────────────────────────

# Sets and reps configuration by fitness level
EXPERIENCE_CONFIG = {
    "beginner": {"sets_range": (2, 3), "reps_range": (8, 10), "rest_seconds": 90, "exercises_per_day": 5},
    "moderate": {"sets_range": (3, 4), "reps_range": (10, 12), "rest_seconds": 60, "exercises_per_day": 6},
    "expert":   {"sets_range": (4, 5), "reps_range": (12, 15), "rest_seconds": 45, "exercises_per_day": 7},
}

# Muscle group splits based on weekly frequency
SPLIT_TEMPLATES = {
    1: [["full_body"]],
    2: [["upper_body"], ["lower_body"]],
    3: [["push"], ["pull"], ["legs"]],
    4: [["push"], ["pull"], ["legs"], ["full_body"]],
    5: [["chest", "triceps"], ["back", "biceps"], ["legs"], ["shoulders", "core"], ["full_body"]],
    6: [["chest"], ["back"], ["shoulders"], ["legs"], ["arms"], ["core"]],
    7: [["chest", "triceps"], ["back", "biceps"], ["legs"], ["shoulders"], ["arms"], ["core"], ["full_body"]],
}

# Mapping split names to target muscle groups for exercise querying
SPLIT_MUSCLE_MAP = {
    "full_body": ["chest", "back", "shoulders", "quadriceps", "hamstrings", "glutes", "core"],
    "upper_body": ["chest", "back", "shoulders", "biceps", "triceps"],
    "lower_body": ["quadriceps", "hamstrings", "glutes", "calves", "core"],
    "push": ["chest", "shoulders", "triceps"],
    "pull": ["back", "biceps", "rear_delts"],
    "legs": ["quadriceps", "hamstrings", "glutes", "calves"],
    "chest": ["chest"],
    "back": ["back"],
    "shoulders": ["shoulders", "rear_delts"],
    "arms": ["biceps", "triceps", "forearms"],
    "core": ["core", "obliques"],
    "triceps": ["triceps"],
    "biceps": ["biceps"],
}

# Medical contraindication → strain area mapping
CONTRAINDICATION_STRAIN_MAP = {
    "spinal_issues": ["strains_lower_back", "strains_upper_back", "spinal_compression"],
    "joint_pain": ["impacts_knees", "impacts_elbows", "impacts_wrists", "impacts_ankles"],
    "knee_injury": ["impacts_knees", "high_knee_stress"],
    "shoulder_injury": ["strains_shoulders", "overhead_strain"],
    "lower_back_pain": ["strains_lower_back", "spinal_compression", "hip_flexor_strain"],
    "wrist_injury": ["impacts_wrists", "grip_strain"],
    "heart_condition": ["high_intensity", "excessive_cardio"],
    "hypertension": ["high_intensity", "overhead_strain"],
    "hip_replacement": ["impacts_hips", "deep_hip_flexion"],
    "neck_issues": ["strains_neck", "cervical_compression"],
    "ankle_injury": ["impacts_ankles", "high_impact"],
}


# ─── Helper Functions ────────────────────────────────────────

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate BMI from height (cm) and weight (kg)."""
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 1)


def get_strain_areas_to_avoid(contraindication_flags: list[str]) -> set[str]:
    """
    Convert user's medical contraindication flags into a set of
    exercise strain areas that should be avoided.
    """
    areas_to_avoid = set()
    for flag in contraindication_flags:
        flag_lower = flag.lower().replace(" ", "_")
        if flag_lower in CONTRAINDICATION_STRAIN_MAP:
            areas_to_avoid.update(CONTRAINDICATION_STRAIN_MAP[flag_lower])
    return areas_to_avoid


def is_exercise_safe(exercise: Exercise, strain_areas_to_avoid: set[str]) -> bool:
    """
    Check if an exercise is safe for the user based on their
    medical contraindication strain areas.
    """
    if not strain_areas_to_avoid:
        return True
    exercise_strains = set(exercise.strain_areas or [])
    # Exercise is unsafe if ANY of its strain areas overlap with areas to avoid
    return len(exercise_strains & strain_areas_to_avoid) == 0


def filter_exercises_by_equipment(
    exercises: list[Exercise],
    available_equipment: list[str],
    training_environment: str,
) -> list[Exercise]:
    """
    Filter exercises based on user's available equipment and
    training environment. Bodyweight exercises are always included.
    """
    filtered = []
    equipment_set = set(eq.lower() for eq in available_equipment)
    # Always include bodyweight
    equipment_set.add("bodyweight")
    equipment_set.add("none")

    for ex in exercises:
        required = ex.equipment_required or []
        # If exercise requires no equipment, include it
        if not required:
            filtered.append(ex)
            continue
        # Check if user has ALL required equipment
        required_set = set(r.lower() for r in required)
        if required_set.issubset(equipment_set):
            filtered.append(ex)

    return filtered


def filter_exercises_by_difficulty(
    exercises: list[Exercise],
    fitness_experience: str,
) -> list[Exercise]:
    """Filter exercises appropriate for the user's experience level."""
    max_difficulty = {"beginner": 1, "moderate": 2, "expert": 3}
    max_diff = max_difficulty.get(fitness_experience, 2)
    return [ex for ex in exercises if (ex.difficulty or 1) <= max_diff]


def find_safe_alternative(
    excluded_exercise: Exercise,
    all_exercises: list[Exercise],
    strain_areas_to_avoid: set[str],
    already_selected_ids: set[int],
) -> Optional[Exercise]:
    """
    Find a safe alternative exercise that targets the same primary muscle
    but doesn't strain the areas that are contraindicated for the user.
    """
    target_muscle = excluded_exercise.target_muscle_primary
    candidates = [
        ex for ex in all_exercises
        if ex.target_muscle_primary == target_muscle
        and ex.exercise_id not in already_selected_ids
        and ex.exercise_id != excluded_exercise.exercise_id
        and is_exercise_safe(ex, strain_areas_to_avoid)
    ]

    if candidates:
        return random.choice(candidates)
    return None


# ─── Main Generation Functions ───────────────────────────────

def select_exercises_for_muscles(
    target_muscles: list[str],
    all_exercises: list[Exercise],
    strain_areas_to_avoid: set[str],
    exercises_per_day: int,
) -> list[Exercise]:
    """
    Select a set of exercises for the given target muscles,
    respecting medical contraindications and finding alternatives
    for unsafe exercises.
    """
    selected = []
    selected_ids = set()

    # Distribute exercises across target muscles
    exercises_per_muscle = max(1, exercises_per_day // len(target_muscles)) if target_muscles else 0
    remaining = exercises_per_day

    for muscle in target_muscles:
        if remaining <= 0:
            break

        # Get exercises targeting this muscle
        muscle_exercises = [
            ex for ex in all_exercises
            if ex.target_muscle_primary.lower() == muscle.lower()
            and ex.exercise_id not in selected_ids
        ]

        count = min(exercises_per_muscle, remaining)

        for ex in muscle_exercises[:count + 2]:  # grab a few extras in case some get filtered
            if len([s for s in selected if s.target_muscle_primary.lower() == muscle.lower()]) >= count:
                break

            if is_exercise_safe(ex, strain_areas_to_avoid):
                selected.append(ex)
                selected_ids.add(ex.exercise_id)
            else:
                # Find a safe alternative
                alt = find_safe_alternative(ex, all_exercises, strain_areas_to_avoid, selected_ids)
                if alt:
                    selected.append(alt)
                    selected_ids.add(alt.exercise_id)

        remaining = exercises_per_day - len(selected)

    return selected[:exercises_per_day]


def build_daily_routine(
    exercises: list[Exercise],
    fitness_experience: str,
) -> list[dict]:
    """
    Build a daily routine JSON structure from selected exercises,
    with sets/reps scaled to the user's fitness experience.
    """
    config = EXPERIENCE_CONFIG.get(fitness_experience, EXPERIENCE_CONFIG["beginner"])
    routine = []

    for ex in exercises:
        sets = random.randint(*config["sets_range"])
        reps = random.randint(*config["reps_range"])
        routine.append({
            "exercise_id": ex.exercise_id,
            "name": ex.name,
            "description": ex.description,
            "target_muscle_primary": ex.target_muscle_primary,
            "target_muscle_secondary": ex.target_muscle_secondary or [],
            "equipment_required": ex.equipment_required or [],
            "difficulty": ex.difficulty,
            "animation_url": ex.animation_url,
            "sets": sets,
            "reps": reps,
            "rest_seconds": config["rest_seconds"],
        })

    return routine


def generate_workout_plan(
    db: Session,
    user: User,
    start_date: Optional[date] = None,
    duration_days: int = 30,
) -> WorkoutPlan:
    """
    Generate a complete workout plan for the user.

    This is the main entry point for workout plan generation.
    It orchestrates the entire pipeline:
    1. Fetch user context (profile + medical history)
    2. Query and filter exercises
    3. Build day-by-day routines
    4. Save to database
    """
    # ── Step 1: Fetch user profile and medical data ──
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.user_id).first()
    if not profile:
        raise ValueError("User profile not found. Complete onboarding first.")

    medical = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first()

    fitness_experience = profile.fitness_experience or "beginner"
    weekly_frequency = profile.weekly_frequency or 3
    preferred_days = profile.preferred_workout_days or []
    available_equipment = profile.available_equipment or []
    training_environment = profile.training_environment or "home"

    # ── Step 2: Get contraindication strain areas ──
    contraindication_flags = medical.contraindication_flags if medical else []
    strain_areas_to_avoid = get_strain_areas_to_avoid(contraindication_flags)

    # ── Step 3: Query and filter exercises ──
    all_exercises = db.query(Exercise).all()

    # Filter by equipment and environment
    filtered_exercises = filter_exercises_by_equipment(
        all_exercises, available_equipment, training_environment
    )

    # Filter by difficulty
    filtered_exercises = filter_exercises_by_difficulty(
        filtered_exercises, fitness_experience
    )

    if not filtered_exercises:
        raise ValueError("No suitable exercises found for your equipment and experience level.")

    # ── Step 4: Determine split template ──
    split = SPLIT_TEMPLATES.get(weekly_frequency, SPLIT_TEMPLATES[3])
    
    # Check for "full body" override in user goals and medical notes
    user_notes = ""
    if profile.goals:
        user_notes += " ".join(profile.goals).lower()
    if medical and medical.medical_notes:
        user_notes += " " + medical.medical_notes.lower()
        
    if "full body" in user_notes or "fullbody" in user_notes:
        split = [["full_body"]] * weekly_frequency
        
    config = EXPERIENCE_CONFIG.get(fitness_experience, EXPERIENCE_CONFIG["beginner"])

    # ── Step 5: Determine workout/rest day schedule ──
    if not start_date:
        start_date = date.today()
    end_date = start_date + timedelta(days=duration_days - 1)

    # Map preferred day names to weekday numbers (0=Monday, 6=Sunday)
    day_name_to_num = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6,
        "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
    }
    preferred_weekdays = set()
    for day_name in preferred_days:
        num = day_name_to_num.get(day_name.lower())
        if num is not None:
            preferred_weekdays.add(num)

    # If no preferred days specified, distribute evenly across the week
    if not preferred_weekdays:
        if weekly_frequency <= 3:
            # Mon, Wed, Fri
            preferred_weekdays = {0, 2, 4}
        elif weekly_frequency <= 5:
            # Mon-Fri
            preferred_weekdays = set(range(weekly_frequency))
        else:
            preferred_weekdays = set(range(7))

    # Adjust to match weekly_frequency
    while len(preferred_weekdays) < weekly_frequency and len(preferred_weekdays) < 7:
        for day in range(7):
            if day not in preferred_weekdays:
                preferred_weekdays.add(day)
                break

    # ── Step 6: Build the plan ──
    plan = WorkoutPlan(
        user_id=user.user_id,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(plan)
    db.flush()  # Get plan_id

    split_index = 0
    current_date = start_date

    while current_date <= end_date:
        weekday = current_date.weekday()

        if weekday in preferred_weekdays:
            # Workout day
            muscle_groups_for_day = split[split_index % len(split)]
            split_index += 1

            # Expand muscle groups using the split map
            target_muscles = []
            day_type_parts = []
            for group in muscle_groups_for_day:
                day_type_parts.append(group)
                muscles = SPLIT_MUSCLE_MAP.get(group, [group])
                target_muscles.extend(muscles)

            # Remove duplicates while preserving order
            seen = set()
            unique_muscles = []
            for m in target_muscles:
                if m not in seen:
                    seen.add(m)
                    unique_muscles.append(m)

            # Select exercises for the day
            day_exercises = select_exercises_for_muscles(
                unique_muscles,
                filtered_exercises,
                strain_areas_to_avoid,
                config["exercises_per_day"],
            )

            # Build the routine
            routine = build_daily_routine(day_exercises, fitness_experience)
            day_type = " + ".join(day_type_parts).title()

            daily = DailyWorkout(
                plan_id=plan.plan_id,
                date=current_date,
                day_type=day_type,
                routine=routine,
            )
        else:
            # Rest day
            daily = DailyWorkout(
                plan_id=plan.plan_id,
                date=current_date,
                day_type="Rest",
                routine=[],
            )

        db.add(daily)
        current_date += timedelta(days=1)

    db.commit()
    db.refresh(plan)

    return plan
