# app/models/session.py

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    device = Column(String(255))
    ip_address = Column(String(255))

    login_time = Column(DateTime(timezone=True), server_default=func.now())
    logout_time = Column(DateTime(timezone=True))
