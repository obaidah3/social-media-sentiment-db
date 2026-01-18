from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Reaction(Base):
    """
    Represents a user's reaction to a post
    (like, love, haha, wow, sad, angry)
    """

    __tablename__ = "reactions"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    reaction_type = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # =========================
    # Constraints & Indexes
    # =========================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_user_post_reaction"
        ),
        Index("ix_reactions_post_id", "post_id"),
        Index("ix_reactions_type", "reaction_type"),
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="reactions"
    )

    post = relationship(
        "Post",
        back_populates="reactions"
    )

    # =========================
    # Helpers
    # =========================

    def __repr__(self) -> str:
        return (
            f"<Reaction user_id={self.user_id} "
            f"post_id={self.post_id} "
            f"type={self.reaction_type}>"
        )
