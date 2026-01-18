# app/schemas/posts.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


# ======================================================
# Sentiment
# ======================================================

class SentimentAnalysis(BaseModel):
    label: str  # positive | neutral | negative
    score: float  # 0.0 → 1.0
    confidence: float  # model confidence
    toxicity: str  # none | low | medium | high


# ======================================================
# Media
# ======================================================

class MediaResponse(BaseModel):
    id: int
    file_url: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# Post Author
# ======================================================

class PostAuthor(BaseModel):
    id: int
    username: str
    profile_pic_url: Optional[str] = None

    class Config:
        from_attributes = True


# ======================================================
# Post Create / Update
# ======================================================

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    visibility: str = Field(
        default="public",
        pattern="^(public|friends|private)$"
    )
    location: Optional[str] = None


class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    visibility: Optional[str] = Field(
        None,
        pattern="^(public|friends|private)$"
    )
    location: Optional[str] = None


# ======================================================
# Post Response
# ======================================================

class PostResponse(BaseModel):
    id: int
    user_id: int
    author: PostAuthor

    content: Optional[str]
    visibility: str
    location: Optional[str]
    platform: str

    created_at: datetime
    updated_at: Optional[datetime]

    # Engagement
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0

    # User flags
    is_liked: bool = False
    is_saved: bool = False

    # Extras
    sentiment: Optional[SentimentAnalysis] = None
    media: List[MediaResponse] = []

    class Config:
        from_attributes = True


# ======================================================
# Comments
# ======================================================

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    parent_id: Optional[int] = None


class CommentAuthor(BaseModel):
    id: int
    username: str
    profile_pic_url: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    parent_id: Optional[int]

    created_at: datetime
    updated_at: Optional[datetime]

    author: CommentAuthor

    likes_count: int = 0
    replies_count: int = 0
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


# ======================================================
# Reactions
# ======================================================

class ReactionCreate(BaseModel):
    reaction_type: str = Field(
        ...,
        pattern="^(like|love|haha|wow|sad|angry)$"
    )


class ReactionResponse(BaseModel):
    total: int
    breakdown: Dict[str, int]
    user_reaction: Optional[str] = None


# ======================================================
# Feed
# ======================================================

class FeedResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


# ======================================================
# Fix forward references
# ======================================================

CommentResponse.model_rebuild()
