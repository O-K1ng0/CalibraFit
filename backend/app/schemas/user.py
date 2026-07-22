"""
CalibraFit — User Pydantic Schemas
Request/response validation models for user, profile, and medical history data.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


# ─── Enums ───────────────────────────────────────────────────

class FitnessExperience(str, Enum):
    beginner = "beginner"
    moderate = "moderate"
    expert = "expert"


class TrainingEnvironment(str, Enum):
    home = "home"
    gym = "gym"


# ─── Auth Schemas ────────────────────────────────────────────

class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, examples=["user@example.com"])
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=255)


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class TokenData(BaseModel):
    user_id: int


class UserResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Profile Schemas ────────────────────────────────────────

class UserProfileCreate(BaseModel):
    age: int = Field(..., ge=13, le=120)
    height_cm: float = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=500)
    fitness_experience: FitnessExperience = FitnessExperience.beginner
    time_since_last_workout_days: int = Field(0, ge=0)
    available_equipment: list[str] = Field(default_factory=list)
    training_environment: TrainingEnvironment = TrainingEnvironment.home
    weekly_frequency: int = Field(3, ge=1, le=7)
    preferred_workout_days: list[str] = Field(default_factory=list)
    preferred_time: str = "morning"
    resting_heart_rate: Optional[int] = Field(None, ge=30, le=220)
    daily_step_count: Optional[int] = Field(None, ge=0)
    body_fat_percentage: Optional[float] = Field(None, ge=1, le=70)


class UserProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=13, le=120)
    height_cm: Optional[float] = Field(None, gt=0, le=300)
    weight_kg: Optional[float] = Field(None, gt=0, le=500)
    fitness_experience: Optional[FitnessExperience] = None
    time_since_last_workout_days: Optional[int] = Field(None, ge=0)
    available_equipment: Optional[list[str]] = None
    training_environment: Optional[TrainingEnvironment] = None
    weekly_frequency: Optional[int] = Field(None, ge=1, le=7)
    preferred_workout_days: Optional[list[str]] = None
    preferred_time: Optional[str] = None
    resting_heart_rate: Optional[int] = Field(None, ge=30, le=220)
    daily_step_count: Optional[int] = Field(None, ge=0)
    body_fat_percentage: Optional[float] = Field(None, ge=1, le=70)


class UserProfileResponse(BaseModel):
    profile_id: int
    user_id: int
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    fitness_experience: str = "beginner"
    time_since_last_workout_days: int = 0
    available_equipment: list[str] = []
    training_environment: str = "home"
    weekly_frequency: int = 3
    preferred_workout_days: list[str] = []
    preferred_time: str = "morning"
    resting_heart_rate: Optional[int] = None
    daily_step_count: Optional[int] = None
    body_fat_percentage: Optional[float] = None

    model_config = {"from_attributes": True}


# ─── Medical History Schemas ─────────────────────────────────

class MedicalHistoryCreate(BaseModel):
    past_surgeries: list[str] = Field(default_factory=list)
    transplants: list[str] = Field(default_factory=list)
    chronic_diseases: list[str] = Field(default_factory=list)
    pain_areas: list[str] = Field(default_factory=list)
    contraindication_flags: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class MedicalHistoryResponse(BaseModel):
    medical_id: int
    profile_id: int
    past_surgeries: list[str] = []
    transplants: list[str] = []
    chronic_diseases: list[str] = []
    pain_areas: list[str] = []
    contraindication_flags: list[str] = []
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


# ─── Complete Profile Response ────────────────────────────────

class FullProfileResponse(BaseModel):
    user: UserResponse
    profile: Optional[UserProfileResponse] = None
    medical_history: Optional[MedicalHistoryResponse] = None
