"""
CalibraFit — SQLAlchemy ORM Models
Maps to the PostgreSQL schema defined in database/schema.sql.
"""

from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Date,
    DateTime, ForeignKey, CheckConstraint, JSON
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    completed_workouts = relationship("CompletedWorkout", back_populates="user", cascade="all, delete-orphan")
    weekly_feedbacks = relationship("WeeklyFeedback", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    age = Column(Integer)
    height_cm = Column(Numeric(5, 1))
    weight_kg = Column(Numeric(5, 1))
    bmi = Column(Numeric(4, 1))
    fitness_experience = Column(String(20), default="beginner")  # beginner, moderate, expert
    time_since_last_workout_days = Column(Integer, default=0)
    available_equipment = Column(JSON, default=list)
    training_environment = Column(String(10), default="home")  # home, gym
    weekly_frequency = Column(Integer, default=3)
    preferred_workout_days = Column(JSON, default=list)
    preferred_time = Column(String(20), default="morning")
    resting_heart_rate = Column(Integer, nullable=True)
    daily_step_count = Column(Integer, nullable=True)
    body_fat_percentage = Column(Numeric(4, 1), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("age >= 13 AND age <= 120", name="check_age_range"),
        CheckConstraint("weekly_frequency >= 1 AND weekly_frequency <= 7", name="check_weekly_frequency"),
    )

    # Relationships
    user = relationship("User", back_populates="profile")
    medical_history = relationship("MedicalHistory", back_populates="profile", uselist=False, cascade="all, delete-orphan")


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    medical_id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.profile_id", ondelete="CASCADE"), unique=True, nullable=False)
    past_surgeries = Column(JSON, default=list)
    transplants = Column(JSON, default=list)
    chronic_diseases = Column(JSON, default=list)
    pain_areas = Column(JSON, default=list)
    contraindication_flags = Column(JSON, default=list)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="medical_history")


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    target_muscle_primary = Column(String(100), nullable=False, index=True)
    target_muscle_secondary = Column(JSON, default=list)
    equipment_required = Column(JSON, default=list)
    difficulty = Column(Integer, default=1, index=True)
    strain_areas = Column(JSON, default=list)
    environment = Column(String(10), default="gym")  # home, gym
    animation_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 3", name="check_difficulty_range"),
    )


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="workout_plans")
    daily_workouts = relationship("DailyWorkout", back_populates="plan", cascade="all, delete-orphan")


class DailyWorkout(Base):
    __tablename__ = "daily_workouts"

    daily_workout_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.plan_id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    day_type = Column(String(50))  # e.g., "push", "pull", "legs", "rest", "full_body"
    routine = Column(JSON, nullable=False, default=list)

    # Relationships
    plan = relationship("WorkoutPlan", back_populates="daily_workouts")
    completions = relationship("CompletedWorkout", back_populates="daily_workout", cascade="all, delete-orphan")


class CompletedWorkout(Base):
    __tablename__ = "completed_workouts"

    completion_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    daily_workout_id = Column(Integer, ForeignKey("daily_workouts.daily_workout_id", ondelete="CASCADE"), nullable=False)
    completed_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    sets_completed = Column(JSON, default=list)
    reps_completed = Column(JSON, default=list)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="completed_workouts")
    daily_workout = relationship("DailyWorkout", back_populates="completions")


class WeeklyFeedback(Base):
    """Stores weekly check-in feedback from the user for adaptive plan regeneration."""
    __tablename__ = "weekly_feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.plan_id", ondelete="CASCADE"), nullable=True)
    week_number = Column(Integer, nullable=False)  # 1, 2, 3, 4...
    difficulty_rating = Column(Integer, nullable=False)  # 1=Too Easy, 2=Just Right, 3=Too Hard
    energy_level = Column(Integer, nullable=True)  # 1-5
    pros = Column(Text, nullable=True)
    cons = Column(Text, nullable=True)
    new_pain_areas = Column(JSON, default=list)  # e.g., ["knees", "shoulders"]
    overall_satisfaction = Column(Integer, nullable=True)  # 1-5 stars
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("difficulty_rating >= 1 AND difficulty_rating <= 3", name="check_difficulty_rating"),
        CheckConstraint("week_number >= 1", name="check_week_number"),
    )

    # Relationships
    user = relationship("User", back_populates="weekly_feedbacks")
