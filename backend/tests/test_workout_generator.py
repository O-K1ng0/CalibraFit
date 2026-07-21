"""
CalibraFit — Unit Tests for Workout Generator Engine
Tests medical filtering, exercise selection, and plan assembly logic.
"""

import pytest
from unittest.mock import MagicMock
from app.core.workout_generator import (
    calculate_bmi,
    get_strain_areas_to_avoid,
    is_exercise_safe,
    filter_exercises_by_equipment,
    filter_exercises_by_difficulty,
    find_safe_alternative,
    select_exercises_for_muscles,
    build_daily_routine,
)


# ─── Fixtures ────────────────────────────────────────────────

def make_exercise(
    exercise_id=1, name="Test Exercise", target_muscle_primary="chest",
    equipment_required=None, difficulty=1, strain_areas=None, environment="home"
):
    """Factory function to create mock Exercise objects."""
    ex = MagicMock()
    ex.exercise_id = exercise_id
    ex.name = name
    ex.description = f"Description for {name}"
    ex.target_muscle_primary = target_muscle_primary
    ex.target_muscle_secondary = []
    ex.equipment_required = equipment_required or []
    ex.difficulty = difficulty
    ex.strain_areas = strain_areas or []
    ex.environment = environment
    ex.animation_url = None
    return ex


# ─── BMI Tests ───────────────────────────────────────────────

class TestCalculateBMI:
    def test_normal_bmi(self):
        bmi = calculate_bmi(175, 70)
        assert 22.0 <= bmi <= 23.0

    def test_zero_height(self):
        bmi = calculate_bmi(0, 70)
        assert bmi == 0.0

    def test_negative_height(self):
        bmi = calculate_bmi(-170, 70)
        assert bmi == 0.0

    def test_obese_bmi(self):
        bmi = calculate_bmi(170, 100)
        assert bmi > 30


# ─── Contraindication Mapping Tests ─────────────────────────

class TestGetStrainAreasToAvoid:
    def test_single_flag(self):
        areas = get_strain_areas_to_avoid(["knee_injury"])
        assert "impacts_knees" in areas
        assert "high_knee_stress" in areas

    def test_multiple_flags(self):
        areas = get_strain_areas_to_avoid(["knee_injury", "lower_back_pain"])
        assert "impacts_knees" in areas
        assert "strains_lower_back" in areas
        assert "spinal_compression" in areas

    def test_empty_flags(self):
        areas = get_strain_areas_to_avoid([])
        assert len(areas) == 0

    def test_unknown_flag(self):
        areas = get_strain_areas_to_avoid(["unknown_condition"])
        assert len(areas) == 0

    def test_case_insensitive(self):
        areas = get_strain_areas_to_avoid(["Knee_Injury"])
        assert "impacts_knees" in areas


# ─── Exercise Safety Tests ──────────────────────────────────

class TestIsExerciseSafe:
    def test_safe_exercise(self):
        ex = make_exercise(strain_areas=["impacts_wrists"])
        assert is_exercise_safe(ex, {"impacts_knees"}) is True

    def test_unsafe_exercise(self):
        ex = make_exercise(strain_areas=["impacts_knees"])
        assert is_exercise_safe(ex, {"impacts_knees"}) is False

    def test_no_strain_areas(self):
        ex = make_exercise(strain_areas=[])
        assert is_exercise_safe(ex, {"impacts_knees"}) is True

    def test_empty_contraindications(self):
        ex = make_exercise(strain_areas=["impacts_knees"])
        assert is_exercise_safe(ex, set()) is True

    def test_multiple_strain_overlap(self):
        ex = make_exercise(strain_areas=["impacts_knees", "strains_lower_back"])
        assert is_exercise_safe(ex, {"strains_lower_back"}) is False


# ─── Equipment Filtering Tests ──────────────────────────────

class TestFilterByEquipment:
    def test_bodyweight_always_included(self):
        exercises = [
            make_exercise(1, "Push-Up", equipment_required=["bodyweight"]),
            make_exercise(2, "Bench Press", equipment_required=["barbell", "bench"]),
        ]
        result = filter_exercises_by_equipment(exercises, [], "home")
        assert len(result) == 1
        assert result[0].name == "Push-Up"

    def test_matching_equipment(self):
        exercises = [
            make_exercise(1, "Push-Up", equipment_required=["bodyweight"]),
            make_exercise(2, "Dumbbell Press", equipment_required=["dumbbells"]),
        ]
        result = filter_exercises_by_equipment(exercises, ["dumbbells"], "home")
        assert len(result) == 2

    def test_missing_equipment(self):
        exercises = [
            make_exercise(1, "Barbell Squat", equipment_required=["barbell", "squat_rack"]),
        ]
        result = filter_exercises_by_equipment(exercises, ["barbell"], "home")
        assert len(result) == 0  # Missing squat_rack

    def test_no_equipment_required(self):
        exercises = [
            make_exercise(1, "Free Exercise", equipment_required=[]),
        ]
        result = filter_exercises_by_equipment(exercises, [], "home")
        assert len(result) == 1


# ─── Difficulty Filtering Tests ─────────────────────────────

class TestFilterByDifficulty:
    def test_beginner_only_level_1(self):
        exercises = [
            make_exercise(1, "Easy", difficulty=1),
            make_exercise(2, "Medium", difficulty=2),
            make_exercise(3, "Hard", difficulty=3),
        ]
        result = filter_exercises_by_difficulty(exercises, "beginner")
        assert len(result) == 1
        assert result[0].difficulty == 1

    def test_moderate_up_to_2(self):
        exercises = [
            make_exercise(1, "Easy", difficulty=1),
            make_exercise(2, "Medium", difficulty=2),
            make_exercise(3, "Hard", difficulty=3),
        ]
        result = filter_exercises_by_difficulty(exercises, "moderate")
        assert len(result) == 2

    def test_expert_all_levels(self):
        exercises = [
            make_exercise(1, "Easy", difficulty=1),
            make_exercise(2, "Medium", difficulty=2),
            make_exercise(3, "Hard", difficulty=3),
        ]
        result = filter_exercises_by_difficulty(exercises, "expert")
        assert len(result) == 3


# ─── Alternative Finding Tests ──────────────────────────────

class TestFindSafeAlternative:
    def test_finds_alternative(self):
        excluded = make_exercise(1, "Squat", target_muscle_primary="quadriceps",
                                 strain_areas=["impacts_knees"])
        alternatives = [
            make_exercise(2, "Leg Extension", target_muscle_primary="quadriceps",
                          strain_areas=["impacts_knees"]),
            make_exercise(3, "Wall Sit", target_muscle_primary="quadriceps",
                          strain_areas=[]),
        ]
        result = find_safe_alternative(excluded, alternatives, {"impacts_knees"}, set())
        assert result is not None
        assert result.exercise_id == 3

    def test_no_alternative_found(self):
        excluded = make_exercise(1, "Squat", target_muscle_primary="quadriceps",
                                 strain_areas=["impacts_knees"])
        alternatives = [
            make_exercise(2, "Lunge", target_muscle_primary="quadriceps",
                          strain_areas=["impacts_knees"]),
        ]
        result = find_safe_alternative(excluded, alternatives, {"impacts_knees"}, set())
        assert result is None

    def test_excludes_already_selected(self):
        excluded = make_exercise(1, "Squat", target_muscle_primary="quadriceps",
                                 strain_areas=["impacts_knees"])
        alternatives = [
            make_exercise(3, "Wall Sit", target_muscle_primary="quadriceps",
                          strain_areas=[]),
        ]
        result = find_safe_alternative(excluded, alternatives, {"impacts_knees"}, {3})
        assert result is None


# ─── Daily Routine Builder Tests ────────────────────────────

class TestBuildDailyRoutine:
    def test_beginner_routine(self):
        exercises = [
            make_exercise(1, "Push-Up"),
            make_exercise(2, "Squat"),
        ]
        routine = build_daily_routine(exercises, "beginner")
        assert len(routine) == 2
        for item in routine:
            assert 2 <= item["sets"] <= 3
            assert 8 <= item["reps"] <= 10
            assert item["rest_seconds"] == 90

    def test_expert_routine(self):
        exercises = [make_exercise(1, "Bench Press")]
        routine = build_daily_routine(exercises, "expert")
        assert len(routine) == 1
        assert 4 <= routine[0]["sets"] <= 5
        assert 12 <= routine[0]["reps"] <= 15
        assert routine[0]["rest_seconds"] == 45

    def test_routine_contains_exercise_info(self):
        exercises = [make_exercise(1, "Push-Up", target_muscle_primary="chest")]
        routine = build_daily_routine(exercises, "moderate")
        assert routine[0]["name"] == "Push-Up"
        assert routine[0]["target_muscle_primary"] == "chest"
        assert "exercise_id" in routine[0]
