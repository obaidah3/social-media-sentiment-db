# app/models/profile.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    name = Column(String(100))
    country = Column(String(100))
    city = Column(String(100))
    phone = Column(String(50))
    birthdate = Column(Date)
    gender = Column(String(20))
    address = Column(String(255))

    platform = Column(String(100))
    handle = Column(String(255))

    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="profile")
