from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
    CheckConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(BigInteger, primary_key=True, index=True)

    # =========================
    # Targets (ONE must exist)
    # =========================

    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=True,
        unique=True,   # ✅ ONE sentiment per post
        index=True
    )

    comment_id = Column(
        BigInteger,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        unique=True,   # ✅ ONE sentiment per comment
        index=True
    )

    # =========================
    # Sentiment Data
    # =========================

    label = Column(String(20), nullable=False)
    score = Column(Float, nullable=False)

    target_type = Column(
        String(20),
        nullable=False
        # post | comment
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    post = relationship(
        "Post",
        back_populates="sentiment",
        foreign_keys=[post_id]
    )

    comment = relationship(
        "Comment",
        back_populates="sentiment",
        foreign_keys=[comment_id]
    )

    # =========================
    # Constraints & Indexes
    # =========================

    __table_args__ = (
        CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR "
            "(post_id IS NULL AND comment_id IS NOT NULL)",
            name="ck_sentiment_single_target"
        ),
        Index("ix_sentiments_target_type", "target_type"),
    )

    def __repr__(self) -> str:
        target_id = self.post_id or self.comment_id
        return f"<Sentiment target={self.target_type} id={target_id} label={self.label}>"
