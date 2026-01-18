# app/api/v1/profiles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile, User
from app.schemas.profiles import ProfileResponse, ProfileUpdate
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


# 🔒 AUTH TODO — WILL WORK LATER
@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile
