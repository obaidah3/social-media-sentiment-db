# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date


class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    # name: str = Field(..., min_length=2, max_length=100)
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()

    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "name": "John Doe",
                "country": "Egypt",
                "city": "Cairo",
                "birthdate": "1990-01-01"
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!"
            }
        }


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str