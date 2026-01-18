# app/models/user_preference.py

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    theme = Column(String(50))
    language = Column(String(50))
    notifications_enabled = Column(Boolean, default=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now())
