# app/schemas/stories.py

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class StoryAuthor(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    title: str
    content: str
    is_published: bool = True


class StoryResponse(BaseModel):
    id: int
    title: str
    content: str
    author: StoryAuthor
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StoriesListResponse(BaseModel):
    stories: List[StoryResponse]
    total: int
