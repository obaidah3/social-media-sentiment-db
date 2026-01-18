from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    String,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    content = Column(Text, nullable=True)

    visibility = Column(
        String(20),
        nullable=False,
        default="public"
    )

    location = Column(String(255), nullable=True)
    platform = Column(String(50), default="web", index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="posts",
        lazy="joined"
    )

    media = relationship(
        "PostMedia",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    reactions = relationship(
        "Reaction",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    bookmarks = relationship(
        "Bookmark",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # ✅ FIXED sentiment relationship
    sentiment = relationship(
        "Sentiment",
        back_populates="post",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="Sentiment.post_id"
    )

    # =========================
    # Indexes
    # =========================

    __table_args__ = (
        Index("ix_posts_visibility", "visibility"),
        Index("ix_posts_created_at", "created_at"),
        Index("ix_posts_user_created", "user_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Post id={self.id} user_id={self.user_id}>"
