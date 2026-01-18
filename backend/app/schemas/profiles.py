# app/schemas/profiles.py

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    platform: Optional[str] = None
    handle: Optional[str] = None


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    followers_count: int
    following_count: int
    created_at: datetime

    class Config:
        from_attributes = True
