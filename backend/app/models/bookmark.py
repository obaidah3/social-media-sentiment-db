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


class Bookmark(Base):
    __tablename__ = "bookmarks"

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

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_user_post_bookmark"
        ),
        Index("idx_bookmarks_user", "user_id"),
        Index("idx_bookmarks_post", "post_id"),
    )

    # ========= Relationships =========

    user = relationship(
        "User",
        back_populates="bookmarks"
    )

    post = relationship(
        "Post",
        back_populates="bookmarks"
    )

    def __repr__(self) -> str:
        return f"<Bookmark user_id={self.user_id} post_id={self.post_id}>"
