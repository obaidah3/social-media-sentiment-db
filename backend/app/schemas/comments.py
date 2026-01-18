from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentAuthor(BaseModel):
    id: int
    username: str
    profile_pic_url: Optional[str] = None


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    author: CommentAuthor
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


CommentResponse.model_rebuild()
