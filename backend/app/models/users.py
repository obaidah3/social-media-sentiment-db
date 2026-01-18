from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # =========================
    # Relationships
    # =========================

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    posts = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    reactions = relationship(
        "Reaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    bookmarks = relationship(
        "Bookmark",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    following = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan"
    )

    followers = relationship(
        "Follow",
        foreign_keys="[Follow.following_id]",
        back_populates="following",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        foreign_keys="Notification.recipient_id",
        back_populates="recipient",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}>"
