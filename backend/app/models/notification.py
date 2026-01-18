# app/models/notification.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, index=True)

    recipient_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    actor_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    type = Column(
        String(30),
        nullable=False
        # follow | like | comment | mention
    )

    object_id = Column(BigInteger, nullable=True)
    object_type = Column(String(30), nullable=True)
    # post | comment | profile

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ========= Relationships =========

    recipient = relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="notifications"
    )

    actor = relationship(
        "User",
        foreign_keys=[actor_id]
    )

    __table_args__ = (
        Index("ix_notifications_recipient_unread", "recipient_id", "is_read"),
    )
