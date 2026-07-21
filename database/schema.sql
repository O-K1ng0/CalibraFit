-- ============================================================
-- CalibraFit — Virtual Personal Trainer Database Schema
-- PostgreSQL (compatible with SQLite for local development)
-- ============================================================

-- Enum types (PostgreSQL only)
DO $$ BEGIN
    CREATE TYPE fitness_experience_level AS ENUM ('beginner', 'moderate', 'expert');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE training_env AS ENUM ('home', 'gym');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ============================================================
-- 1. USERS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id         SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================================
-- 2. USER PROFILES
-- ============================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id              SERIAL PRIMARY KEY,
    user_id                 INTEGER UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    age                     INTEGER CHECK (age >= 13 AND age <= 120),
    height_cm               NUMERIC(5, 1),
    weight_kg               NUMERIC(5, 1),
    bmi                     NUMERIC(4, 1),
    fitness_experience      fitness_experience_level DEFAULT 'beginner',
    time_since_last_workout_days INTEGER DEFAULT 0,
    available_equipment     JSONB DEFAULT '[]'::jsonb,
    training_environment    training_env DEFAULT 'home',
    weekly_frequency        INTEGER DEFAULT 3 CHECK (weekly_frequency >= 1 AND weekly_frequency <= 7),
    preferred_workout_days  JSONB DEFAULT '[]'::jsonb,
    preferred_time          VARCHAR(20) DEFAULT 'morning',
    resting_heart_rate      INTEGER,
    daily_step_count        INTEGER,
    body_fat_percentage     NUMERIC(4, 1),
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- 3. MEDICAL HISTORY
-- ============================================================
CREATE TABLE IF NOT EXISTS medical_history (
    medical_id              SERIAL PRIMARY KEY,
    profile_id              INTEGER UNIQUE NOT NULL REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    past_surgeries          JSONB DEFAULT '[]'::jsonb,
    transplants             JSONB DEFAULT '[]'::jsonb,
    chronic_diseases        JSONB DEFAULT '[]'::jsonb,
    pain_areas              JSONB DEFAULT '[]'::jsonb,
    contraindication_flags  JSONB DEFAULT '[]'::jsonb,
    notes                   TEXT,
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- 4. EXERCISES
-- ============================================================
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id             SERIAL PRIMARY KEY,
    name                    VARCHAR(255) NOT NULL,
    description             TEXT,
    target_muscle_primary   VARCHAR(100) NOT NULL,
    target_muscle_secondary JSONB DEFAULT '[]'::jsonb,
    equipment_required      JSONB DEFAULT '[]'::jsonb,
    difficulty              INTEGER CHECK (difficulty >= 1 AND difficulty <= 3) DEFAULT 1,
    strain_areas            JSONB DEFAULT '[]'::jsonb,
    environment             training_env DEFAULT 'gym',
    animation_url           TEXT,
    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_exercises_muscle ON exercises(target_muscle_primary);
CREATE INDEX IF NOT EXISTS idx_exercises_difficulty ON exercises(difficulty);

-- ============================================================
-- 5. WORKOUT PLANS
-- ============================================================
CREATE TABLE IF NOT EXISTS workout_plans (
    plan_id                 SERIAL PRIMARY KEY,
    user_id                 INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    start_date              DATE NOT NULL,
    end_date                DATE NOT NULL,
    generated_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_plans_user ON workout_plans(user_id);

-- ============================================================
-- 6. DAILY WORKOUTS
-- ============================================================
CREATE TABLE IF NOT EXISTS daily_workouts (
    daily_workout_id        SERIAL PRIMARY KEY,
    plan_id                 INTEGER NOT NULL REFERENCES workout_plans(plan_id) ON DELETE CASCADE,
    date                    DATE NOT NULL,
    day_type                VARCHAR(50),
    routine                 JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_daily_workouts_plan ON daily_workouts(plan_id);
CREATE INDEX IF NOT EXISTS idx_daily_workouts_date ON daily_workouts(date);

-- ============================================================
-- 7. COMPLETED WORKOUTS
-- ============================================================
CREATE TABLE IF NOT EXISTS completed_workouts (
    completion_id           SERIAL PRIMARY KEY,
    user_id                 INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    daily_workout_id        INTEGER NOT NULL REFERENCES daily_workouts(daily_workout_id) ON DELETE CASCADE,
    completed_at            TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sets_completed          JSONB DEFAULT '[]'::jsonb,
    reps_completed          JSONB DEFAULT '[]'::jsonb,
    duration_minutes        INTEGER,
    notes                   TEXT
);

CREATE INDEX IF NOT EXISTS idx_completed_workouts_user ON completed_workouts(user_id);
CREATE INDEX IF NOT EXISTS idx_completed_workouts_date ON completed_workouts(completed_at);
