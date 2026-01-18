# app/models/post_media.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class PostMedia(Base):
    __tablename__ = "post_media"

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

    file_url = Column(
        String(500),
        nullable=False
    )

    file_type = Column(
        String(20),
        nullable=False
    )
    # image | video | gif | audio (future-proof)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # =======================
    # Relationships
    # =======================

    post = relationship(
        "Post",
        back_populates="media"
    )

    # =======================
    # Indexes
    # =======================

    __table_args__ = (
        Index("idx_post_media_post_created", "post_id", "created_at"),
    )

    # =======================
    # Helpers
    # =======================

    def __repr__(self) -> str:
        return f"<PostMedia id={self.id} post_id={self.post_id} type={self.file_type}>"
