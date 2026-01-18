# app/core/jwt.py

from typing import Optional, Dict
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.config import settings

ALGORITHM = settings.ALGORITHM


def create_access_token(
    subject: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": str(subject),           # JWT standard = string
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    subject: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.utcnow() + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    payload = {
        "sub": str(subject),
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError as e:
        print("JWT ERROR:", e)
        return None
