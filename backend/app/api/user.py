"""
CalibraFit — User Profile & Medical History API Endpoints
CRUD operations for user profiles and medical data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User, UserProfile, MedicalHistory
from app.schemas.user import (
    UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    MedicalHistoryCreate, MedicalHistoryResponse,
    FullProfileResponse, UserResponse,
)
from app.core.security import get_current_user
from app.core.workout_generator import calculate_bmi

router = APIRouter(prefix="/api/user", tags=["User Profile"])


# ─── Profile Endpoints ──────────────────────────────────────

@router.post("/profile", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create user profile during onboarding."""
    # Check if profile already exists
    existing = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update.",
        )

    # Calculate BMI
    bmi = calculate_bmi(profile_data.height_cm, profile_data.weight_kg)

    profile = UserProfile(
        user_id=current_user.user_id,
        age=profile_data.age,
        height_cm=profile_data.height_cm,
        weight_kg=profile_data.weight_kg,
        bmi=bmi,
        fitness_experience=profile_data.fitness_experience.value,
        time_since_last_workout_days=profile_data.time_since_last_workout_days,
        available_equipment=profile_data.available_equipment,
        training_environment=profile_data.training_environment.value,
        weekly_frequency=profile_data.weekly_frequency,
        preferred_workout_days=profile_data.preferred_workout_days,
        preferred_time=profile_data.preferred_time,
        resting_heart_rate=profile_data.resting_heart_rate,
        daily_step_count=profile_data.daily_step_count,
        body_fat_percentage=profile_data.body_fat_percentage,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    update_data = profile_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(profile, field):
            # Convert enum values to strings
            if hasattr(value, 'value'):
                value = value.value
            setattr(profile, field, value)

    # Recalculate BMI if height or weight changed
    if "height_cm" in update_data or "weight_kg" in update_data:
        height = float(profile.height_cm) if profile.height_cm else 0
        weight = float(profile.weight_kg) if profile.weight_kg else 0
        profile.bmi = calculate_bmi(height, weight)

    db.commit()
    db.refresh(profile)

    return profile


# ─── Medical History Endpoints ───────────────────────────────

@router.post("/medical-history", response_model=MedicalHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_medical_history(
    medical_data: MedicalHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save user's medical history during onboarding."""
    # Get profile first
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Create a profile first before adding medical history.",
        )

    # Check if medical history already exists
    existing = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first()
    if existing:
        # Update existing record instead
        for field, value in medical_data.model_dump().items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    medical = MedicalHistory(
        profile_id=profile.profile_id,
        past_surgeries=medical_data.past_surgeries,
        transplants=medical_data.transplants,
        chronic_diseases=medical_data.chronic_diseases,
        pain_areas=medical_data.pain_areas,
        contraindication_flags=medical_data.contraindication_flags,
        notes=medical_data.notes,
    )
    db.add(medical)
    db.commit()
    db.refresh(medical)

    return medical


@router.get("/medical-history", response_model=MedicalHistoryResponse)
def get_medical_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's medical history."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    medical = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first()
    if not medical:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical history not found")

    return medical


@router.put("/medical-history", response_model=MedicalHistoryResponse)
def update_medical_history(
    medical_data: MedicalHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's medical history."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    medical = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first()
    if not medical:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical history not found")

    for field, value in medical_data.model_dump().items():
        setattr(medical, field, value)

    db.commit()
    db.refresh(medical)

    return medical


# ─── Full Profile ────────────────────────────────────────────

@router.get("/full-profile", response_model=FullProfileResponse)
def get_full_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get complete user profile including medical history."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()
    medical = None
    if profile:
        medical = db.query(MedicalHistory).filter(MedicalHistory.profile_id == profile.profile_id).first()

    return FullProfileResponse(
        user=UserResponse.model_validate(current_user),
        profile=UserProfileResponse.model_validate(profile) if profile else None,
        medical_history=MedicalHistoryResponse.model_validate(medical) if medical else None,
    )
