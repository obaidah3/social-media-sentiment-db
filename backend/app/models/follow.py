from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(BigInteger, primary_key=True, index=True)

    follower_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    following_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="uq_follower_following"
        ),
        Index("ix_follows_follower", "follower_id"),
        Index("ix_follows_following", "following_id"),
    )

    # ========= Relationships =========

    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    following = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers"
    )

    def __repr__(self) -> str:
        return f"<Follow {self.follower_id} -> {self.following_id}>"
