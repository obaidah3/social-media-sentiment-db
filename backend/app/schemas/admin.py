# app/schemas/admin.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class ModerationAction(BaseModel):
    """Moderation action"""
    action: str = Field(..., pattern="^(approve|remove|suspend_user|warn)$")
    reason: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "action": "remove",
                "reason": "Toxic content violation"
            }
        }


class FlaggedContent(BaseModel):
    """Flagged content for review"""
    content_id: int
    content_type: str  # 'post' or 'comment'
    content_text: str
    author_id: int
    author_username: str
    sentiment_label: str
    toxicity_level: str
    flag_count: int
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "content_id": 1,
                "content_type": "post",
                "content_text": "This is harmful content...",
                "author_id": 5,
                "author_username": "baduser",
                "sentiment_label": "negative",
                "toxicity_level": "high",
                "flag_count": 3,
                "created_at": "2024-01-15T10:30:00"
            }
        }


class UserManagement(BaseModel):
    """User management action"""
    user_id: int
    action: str = Field(..., pattern="^(suspend|unsuspend|delete|make_admin|remove_admin)$")
    reason: Optional[str] = None


class SystemStats(BaseModel):
    """System-wide statistics"""
    total_users: int
    active_users_today: int
    total_posts: int
    posts_today: int
    total_comments: int
    comments_today: int
    flagged_content_count: int
    suspended_users_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_users": 1500,
                "active_users_today": 234,
                "total_posts": 5000,
                "posts_today": 120,
                "total_comments": 15000,
                "comments_today": 450,
                "flagged_content_count": 5,
                "suspended_users_count": 2
            }
        }


class UserDetail(BaseModel):
    """Detailed user information for admin"""
    User_id: int
    Username: str
    Email: str
    Date_Joined: date
    Country: Optional[str]
    role: str = "user"
    status: str = "active"
    posts_count: int
    comments_count: int
    followers_count: int
    following_count: int
    flags_received: int

    class Config:
        from_attributes = True