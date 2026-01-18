from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    # =======================
    # Primary Fields
    # =======================

    id = Column(BigInteger, primary_key=True, index=True)

    post_id = Column(
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    parent_id = Column(
        BigInteger,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    content = Column(Text, nullable=False)

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

    # =======================
    # Relationships
    # =======================

    # Author
    user = relationship(
        "User",
        back_populates="comments"
    )

    # Post
    post = relationship(
        "Post",
        back_populates="comments"
    )

    # ✅ Self-referencing (FIXED)
    parent = relationship(
        "Comment",
        remote_side=[id],
        back_populates="replies"
    )

    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # Sentiment (1–1)
    sentiment = relationship(
        "Sentiment",
        back_populates="comment",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # =======================
    # Indexes
    # =======================

    __table_args__ = (
        Index("idx_comments_post_created", "post_id", "created_at"),
        Index("idx_comments_user_created", "user_id", "created_at"),
        Index("idx_comments_parent", "parent_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<Comment id={self.id} "
            f"post_id={self.post_id} "
            f"user_id={self.user_id} "
            f"parent_id={self.parent_id}>"
        )
