"""
CalibraFit — Exercise Seed Data Script
Populates the database with ~60 exercises across all muscle groups.
Run: python seed_exercises.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, create_tables
from app.db.models import Exercise

EXERCISES = [
    # ─── CHEST ───────────────────────────────────────────────
    {
        "name": "Push-Ups",
        "description": "Classic bodyweight exercise targeting the chest, shoulders, and triceps. Keep core tight and body in a straight line.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["triceps", "shoulders", "core"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["impacts_wrists"],
        "environment": "home",
        "animation_url": "https://assets10.lottiefiles.com/packages/lf20_push_ups.json",
    },
    {
        "name": "Incline Push-Ups",
        "description": "Hands elevated on a bench or step. Easier variation that targets upper chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["triceps", "shoulders"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Dumbbell Bench Press",
        "description": "Lie on a flat bench and press dumbbells upward. Great for chest development and stabilizer activation.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["triceps", "shoulders"],
        "equipment_required": ["dumbbells", "bench"],
        "difficulty": 2,
        "strain_areas": ["strains_shoulders"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Barbell Bench Press",
        "description": "The king of chest exercises. Lie on a bench and press a barbell upward from chest level.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["triceps", "shoulders"],
        "equipment_required": ["barbell", "bench"],
        "difficulty": 3,
        "strain_areas": ["strains_shoulders", "impacts_wrists"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Dumbbell Flyes",
        "description": "Lie on a bench with dumbbells extended, lower them in an arc to stretch the chest, then squeeze back up.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["shoulders"],
        "equipment_required": ["dumbbells", "bench"],
        "difficulty": 2,
        "strain_areas": ["strains_shoulders"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Resistance Band Chest Press",
        "description": "Anchor band behind you and press forward at chest height. Great home alternative to bench press.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": ["triceps", "shoulders"],
        "equipment_required": ["resistance_bands"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },

    # ─── BACK ────────────────────────────────────────────────
    {
        "name": "Bodyweight Rows (Inverted Rows)",
        "description": "Hang under a bar and pull your chest up. Adjustable difficulty by changing body angle.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["biceps", "rear_delts"],
        "equipment_required": ["pull_up_bar"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Pull-Ups",
        "description": "Hang from a bar and pull yourself up until chin is over the bar. Premier back exercise.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["biceps", "forearms"],
        "equipment_required": ["pull_up_bar"],
        "difficulty": 2,
        "strain_areas": ["strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Dumbbell Rows",
        "description": "Bend over with one hand on a bench, row a dumbbell up to your hip. Targets lats and middle back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["biceps", "rear_delts"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["strains_lower_back"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Barbell Bent-Over Rows",
        "description": "Hinge at hips holding a barbell, row it to your lower chest. Builds a thick, strong back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["biceps", "rear_delts", "core"],
        "equipment_required": ["barbell"],
        "difficulty": 3,
        "strain_areas": ["strains_lower_back", "strains_upper_back"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Lat Pulldowns",
        "description": "Sit at a cable machine and pull the bar down to your upper chest. Builds lat width.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["biceps"],
        "equipment_required": ["cable_machine"],
        "difficulty": 1,
        "strain_areas": ["strains_shoulders"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Resistance Band Pull-Aparts",
        "description": "Hold a band at arm's length and pull it apart to shoulder width. Excellent for rear delts and upper back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["rear_delts", "shoulders"],
        "equipment_required": ["resistance_bands"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Superman Hold",
        "description": "Lie face down and lift arms and legs off the floor simultaneously. Strengthens the posterior chain.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": ["glutes", "core"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["strains_lower_back"],
        "environment": "home",
        "animation_url": None,
    },

    # ─── SHOULDERS ───────────────────────────────────────────
    {
        "name": "Pike Push-Ups",
        "description": "Push-up with hips elevated high, shifting focus to shoulders. A bodyweight overhead press alternative.",
        "target_muscle_primary": "shoulders",
        "target_muscle_secondary": ["triceps", "core"],
        "equipment_required": ["bodyweight"],
        "difficulty": 2,
        "strain_areas": ["overhead_strain", "impacts_wrists"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Dumbbell Shoulder Press",
        "description": "Seated or standing, press dumbbells overhead from shoulder height. Primary shoulder builder.",
        "target_muscle_primary": "shoulders",
        "target_muscle_secondary": ["triceps"],
        "equipment_required": ["dumbbells"],
        "difficulty": 2,
        "strain_areas": ["overhead_strain", "strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Lateral Raises",
        "description": "Stand with dumbbells at sides, raise them out to shoulder height. Isolates medial deltoids.",
        "target_muscle_primary": "shoulders",
        "target_muscle_secondary": [],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Front Raises",
        "description": "Raise dumbbells in front of you to shoulder height. Targets anterior deltoids.",
        "target_muscle_primary": "shoulders",
        "target_muscle_secondary": ["chest"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Band Face Pulls",
        "description": "Pull a resistance band toward your face with elbows high. Great for rear delts and rotator cuff health.",
        "target_muscle_primary": "rear_delts",
        "target_muscle_secondary": ["shoulders", "back"],
        "equipment_required": ["resistance_bands"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Arnold Press",
        "description": "A rotational dumbbell press named after Arnold Schwarzenegger. Hits all three heads of the deltoids.",
        "target_muscle_primary": "shoulders",
        "target_muscle_secondary": ["triceps"],
        "equipment_required": ["dumbbells"],
        "difficulty": 3,
        "strain_areas": ["overhead_strain", "strains_shoulders"],
        "environment": "gym",
        "animation_url": None,
    },

    # ─── BICEPS ──────────────────────────────────────────────
    {
        "name": "Dumbbell Bicep Curls",
        "description": "Stand and curl dumbbells from waist to shoulder. The staple bicep exercise.",
        "target_muscle_primary": "biceps",
        "target_muscle_secondary": ["forearms"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["impacts_elbows"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Hammer Curls",
        "description": "Curl dumbbells with a neutral (hammer) grip. Targets brachialis and forearms.",
        "target_muscle_primary": "biceps",
        "target_muscle_secondary": ["forearms"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Resistance Band Curls",
        "description": "Stand on a band and curl upward. Progressive resistance throughout the range of motion.",
        "target_muscle_primary": "biceps",
        "target_muscle_secondary": ["forearms"],
        "equipment_required": ["resistance_bands"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Barbell Curls",
        "description": "Stand and curl a barbell from thighs to chest. Allows heavier loading than dumbbells.",
        "target_muscle_primary": "biceps",
        "target_muscle_secondary": ["forearms"],
        "equipment_required": ["barbell"],
        "difficulty": 2,
        "strain_areas": ["impacts_wrists", "impacts_elbows"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Chin-Ups",
        "description": "Pull-up with an underhand grip. Heavily targets biceps while also working the back.",
        "target_muscle_primary": "biceps",
        "target_muscle_secondary": ["back", "forearms"],
        "equipment_required": ["pull_up_bar"],
        "difficulty": 2,
        "strain_areas": ["strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },

    # ─── TRICEPS ─────────────────────────────────────────────
    {
        "name": "Diamond Push-Ups",
        "description": "Push-ups with hands close together forming a diamond shape. Emphasizes triceps.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": ["chest", "shoulders"],
        "equipment_required": ["bodyweight"],
        "difficulty": 2,
        "strain_areas": ["impacts_wrists", "impacts_elbows"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Tricep Dips (Bench)",
        "description": "Place hands on a bench behind you, lower and press up. Effective bodyweight tricep exercise.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": ["chest", "shoulders"],
        "equipment_required": ["bench"],
        "difficulty": 1,
        "strain_areas": ["strains_shoulders", "impacts_elbows"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Overhead Tricep Extension",
        "description": "Hold a dumbbell overhead and lower it behind your head, then extend back up.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": [],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["overhead_strain", "impacts_elbows"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Tricep Kickbacks",
        "description": "Bend over, hold a dumbbell, and extend your arm straight back. Isolates the triceps.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": [],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["impacts_elbows"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Cable Tricep Pushdowns",
        "description": "At a cable machine, push the bar down from chest to thighs. Keeps constant tension on triceps.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": [],
        "equipment_required": ["cable_machine"],
        "difficulty": 1,
        "strain_areas": ["impacts_elbows"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Skull Crushers",
        "description": "Lie on a bench and lower a barbell/dumbbell toward your forehead, then extend.",
        "target_muscle_primary": "triceps",
        "target_muscle_secondary": [],
        "equipment_required": ["barbell", "bench"],
        "difficulty": 3,
        "strain_areas": ["impacts_elbows", "impacts_wrists"],
        "environment": "gym",
        "animation_url": None,
    },

    # ─── QUADRICEPS ──────────────────────────────────────────
    {
        "name": "Bodyweight Squats",
        "description": "Stand with feet shoulder-width apart, lower hips down and back, then stand up. Fundamental leg exercise.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes", "hamstrings", "core"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["impacts_knees"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Goblet Squats",
        "description": "Hold a dumbbell at your chest and squat. Promotes good squat form and depth.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes", "core"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["impacts_knees"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Walking Lunges",
        "description": "Step forward into a lunge, then bring the back foot forward. Repeat while walking forward.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes", "hamstrings"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["impacts_knees", "impacts_ankles"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Barbell Back Squats",
        "description": "Place a barbell on your upper back and squat. The king of leg exercises for overall lower body development.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes", "hamstrings", "core"],
        "equipment_required": ["barbell", "squat_rack"],
        "difficulty": 3,
        "strain_areas": ["impacts_knees", "strains_lower_back", "spinal_compression"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Leg Press",
        "description": "Sit in a leg press machine and push the platform away with your feet.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes", "hamstrings"],
        "equipment_required": ["leg_press_machine"],
        "difficulty": 2,
        "strain_areas": ["impacts_knees"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Wall Sits",
        "description": "Lean against a wall in a seated position and hold. Isometric quad strength builder.",
        "target_muscle_primary": "quadriceps",
        "target_muscle_secondary": ["glutes"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["high_knee_stress"],
        "environment": "home",
        "animation_url": None,
    },

    # ─── HAMSTRINGS ──────────────────────────────────────────
    {
        "name": "Romanian Deadlifts (Dumbbell)",
        "description": "Hinge at hips with dumbbells, lowering them along your shins. Stretches and strengthens hamstrings.",
        "target_muscle_primary": "hamstrings",
        "target_muscle_secondary": ["glutes", "back"],
        "equipment_required": ["dumbbells"],
        "difficulty": 2,
        "strain_areas": ["strains_lower_back"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Glute Bridges",
        "description": "Lie on your back, feet flat, and push hips upward. Also targets glutes.",
        "target_muscle_primary": "hamstrings",
        "target_muscle_secondary": ["glutes", "core"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Nordic Hamstring Curls",
        "description": "Kneel and lower your body forward under control. Advanced hamstring exercise.",
        "target_muscle_primary": "hamstrings",
        "target_muscle_secondary": [],
        "equipment_required": ["bodyweight"],
        "difficulty": 3,
        "strain_areas": ["impacts_knees"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Lying Leg Curls",
        "description": "Lie face down on a leg curl machine and curl your heels toward your glutes.",
        "target_muscle_primary": "hamstrings",
        "target_muscle_secondary": [],
        "equipment_required": ["leg_curl_machine"],
        "difficulty": 1,
        "strain_areas": ["impacts_knees"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Good Mornings",
        "description": "With a barbell on your back, hinge at the hips. Targets hamstrings and lower back.",
        "target_muscle_primary": "hamstrings",
        "target_muscle_secondary": ["back", "glutes"],
        "equipment_required": ["barbell"],
        "difficulty": 3,
        "strain_areas": ["strains_lower_back", "spinal_compression"],
        "environment": "gym",
        "animation_url": None,
    },

    # ─── GLUTES ──────────────────────────────────────────────
    {
        "name": "Hip Thrusts",
        "description": "Lean upper back against a bench, place barbell or dumbbell on hips, and thrust upward.",
        "target_muscle_primary": "glutes",
        "target_muscle_secondary": ["hamstrings", "core"],
        "equipment_required": ["bench", "dumbbells"],
        "difficulty": 2,
        "strain_areas": ["deep_hip_flexion"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Glute Bridges (Weighted)",
        "description": "Lie on your back with a weight on your hips and thrust upward. Targeted glute activation.",
        "target_muscle_primary": "glutes",
        "target_muscle_secondary": ["hamstrings"],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Bulgarian Split Squats",
        "description": "Rear foot elevated on a bench, squat on front leg. Excellent unilateral glute and quad exercise.",
        "target_muscle_primary": "glutes",
        "target_muscle_secondary": ["quadriceps", "hamstrings"],
        "equipment_required": ["bench"],
        "difficulty": 2,
        "strain_areas": ["impacts_knees", "impacts_ankles"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Donkey Kicks",
        "description": "On hands and knees, kick one leg back and up. Isolates the glutes.",
        "target_muscle_primary": "glutes",
        "target_muscle_secondary": [],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },

    # ─── CALVES ──────────────────────────────────────────────
    {
        "name": "Standing Calf Raises",
        "description": "Stand on the edge of a step and raise your heels. Simple but effective calf builder.",
        "target_muscle_primary": "calves",
        "target_muscle_secondary": [],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["impacts_ankles"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Seated Calf Raises",
        "description": "Sit with weight on your knees and raise your heels. Targets the soleus muscle.",
        "target_muscle_primary": "calves",
        "target_muscle_secondary": [],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Jump Rope",
        "description": "Skip rope at a steady pace. Great cardio and calf conditioning exercise.",
        "target_muscle_primary": "calves",
        "target_muscle_secondary": ["core", "shoulders"],
        "equipment_required": ["jump_rope"],
        "difficulty": 1,
        "strain_areas": ["impacts_knees", "impacts_ankles", "high_impact"],
        "environment": "home",
        "animation_url": None,
    },

    # ─── CORE ────────────────────────────────────────────────
    {
        "name": "Plank",
        "description": "Hold a push-up position on your forearms. Foundation core stabilization exercise.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": ["shoulders"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["strains_lower_back"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Dead Bugs",
        "description": "Lie on your back and alternately extend opposite arm and leg. Safe and effective core exercise.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": [],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Mountain Climbers",
        "description": "In plank position, drive knees toward chest alternately. Cardio and core in one.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": ["shoulders", "quadriceps"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["impacts_wrists", "high_intensity"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Bicycle Crunches",
        "description": "Lie on your back and pedal your legs while touching opposite elbow to knee.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": ["obliques"],
        "equipment_required": ["bodyweight"],
        "difficulty": 1,
        "strain_areas": ["strains_neck"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Hanging Leg Raises",
        "description": "Hang from a bar and raise your legs to hip level. Advanced core exercise.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": ["hip_flexors"],
        "equipment_required": ["pull_up_bar"],
        "difficulty": 3,
        "strain_areas": ["strains_shoulders", "hip_flexor_strain"],
        "environment": "gym",
        "animation_url": None,
    },
    {
        "name": "Russian Twists",
        "description": "Sit with knees bent, lean back slightly, and rotate a weight side to side.",
        "target_muscle_primary": "obliques",
        "target_muscle_secondary": ["core"],
        "equipment_required": ["dumbbells"],
        "difficulty": 2,
        "strain_areas": ["strains_lower_back"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Ab Wheel Rollouts",
        "description": "Kneel and roll an ab wheel forward, then pull yourself back. Advanced core challenge.",
        "target_muscle_primary": "core",
        "target_muscle_secondary": ["shoulders", "back"],
        "equipment_required": ["ab_wheel"],
        "difficulty": 3,
        "strain_areas": ["strains_lower_back", "strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Side Plank",
        "description": "Support your body on one forearm and the side of your foot. Targets obliques and lateral core.",
        "target_muscle_primary": "obliques",
        "target_muscle_secondary": ["core", "shoulders"],
        "equipment_required": ["bodyweight"],
        "difficulty": 2,
        "strain_areas": ["strains_shoulders"],
        "environment": "home",
        "animation_url": None,
    },

    # ─── FOREARMS ────────────────────────────────────────────
    {
        "name": "Wrist Curls",
        "description": "Sit with forearms resting on thighs, curl a dumbbell with your wrists.",
        "target_muscle_primary": "forearms",
        "target_muscle_secondary": [],
        "equipment_required": ["dumbbells"],
        "difficulty": 1,
        "strain_areas": ["impacts_wrists"],
        "environment": "home",
        "animation_url": None,
    },
    {
        "name": "Farmer's Walk",
        "description": "Hold heavy dumbbells at your sides and walk for distance or time. Total body conditioning.",
        "target_muscle_primary": "forearms",
        "target_muscle_secondary": ["core", "shoulders", "back"],
        "equipment_required": ["dumbbells"],
        "difficulty": 2,
        "strain_areas": ["grip_strain"],
        "environment": "home",
        "animation_url": None,
    },
]


def seed_exercises():
    """Seed the database with the exercise data."""
    db = SessionLocal()
    try:
        # Check if exercises already exist
        existing_count = db.query(Exercise).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} exercises. Skipping seed.")
            print("To re-seed, delete existing exercises first.")
            return

        for ex_data in EXERCISES:
            exercise = Exercise(**ex_data)
            db.add(exercise)

        db.commit()
        print(f"✅ Successfully seeded {len(EXERCISES)} exercises!")

        # Print summary
        muscles = {}
        for ex in EXERCISES:
            m = ex["target_muscle_primary"]
            muscles[m] = muscles.get(m, 0) + 1

        print("\nExercises by muscle group:")
        for muscle, count in sorted(muscles.items()):
            print(f"  {muscle}: {count}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding exercises: {e}")
        raise
    finally:
        db.close()


NEW_EXERCISES = [
    {
        "name": "Incline Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bodyweight Press",
        "description": "A bodyweight variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bodyweight Fly",
        "description": "A bodyweight variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bodyweight Push-Up",
        "description": "A bodyweight variation of the Push-Up targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bodyweight Pullover",
        "description": "A bodyweight variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Dumbbells Press",
        "description": "A dumbbells variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Dumbbells Fly",
        "description": "A dumbbells variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Dumbbells Pullover",
        "description": "A dumbbells variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "dumbbells"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Barbell Press",
        "description": "A barbell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Barbell Fly",
        "description": "A barbell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Barbell Pullover",
        "description": "A barbell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "barbell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Kettlebell Press",
        "description": "A kettlebell variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Kettlebell Fly",
        "description": "A kettlebell variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Kettlebell Pullover",
        "description": "A kettlebell variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "kettlebell"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Standing Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Weighted Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Banded Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bands Press",
        "description": "A bands variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bands Fly",
        "description": "A bands variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Explosive Bands Pullover",
        "description": "A bands variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bands"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Cable Press",
        "description": "A cable variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Cable Fly",
        "description": "A cable variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Cable Pullover",
        "description": "A cable variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "cable"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Decline Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Seated Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Standing Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Arm Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Single-Leg Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Weighted Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Banded Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 1,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Machine Press",
        "description": "A machine variation of the Press targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Machine Fly",
        "description": "A machine variation of the Fly targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Explosive Machine Pullover",
        "description": "A machine variation of the Pullover targeting the chest.",
        "target_muscle_primary": "chest",
        "target_muscle_secondary": [],
        "equipment_required": [
            "machine"
        ],
        "difficulty": 2,
        "strain_areas": [],
        "environment": "gym",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Row",
        "description": "A bodyweight variation of the Row targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Pulldown",
        "description": "A bodyweight variation of the Pulldown targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "shoulder_injury",
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Pull-Up",
        "description": "A bodyweight variation of the Pull-Up targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Incline Bodyweight Deadlift",
        "description": "A bodyweight variation of the Deadlift targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Row",
        "description": "A bodyweight variation of the Row targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Pulldown",
        "description": "A bodyweight variation of the Pulldown targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "shoulder_injury",
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Pull-Up",
        "description": "A bodyweight variation of the Pull-Up targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Decline Bodyweight Deadlift",
        "description": "A bodyweight variation of the Deadlift targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Row",
        "description": "A bodyweight variation of the Row targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    },
    {
        "name": "Seated Bodyweight Pulldown",
        "description": "A bodyweight variation of the Pulldown targeting the back.",
        "target_muscle_primary": "back",
        "target_muscle_secondary": [],
        "equipment_required": [
            "bodyweight"
        ],
        "difficulty": 1,
        "strain_areas": [
            "shoulder_injury",
            "lower_back_pain"
        ],
        "environment": "home",
        "animation_url": ""
    }
]
EXERCISES.extend(NEW_EXERCISES)

if __name__ == "__main__":
    print("🌱 Seeding CalibraFit exercise database...")
    create_tables()
    seed_exercises()
