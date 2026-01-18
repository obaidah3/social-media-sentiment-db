from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationActor(BaseModel):
    id: int
    username: str
    profile_pic_url: Optional[str] = None

    class Config:
        orm_mode = True


class NotificationResponse(BaseModel):
    id: int
    type: str
    object_id: Optional[int]
    object_type: Optional[str]
    is_read: bool
    created_at: datetime
    actor: NotificationActor

    class Config:
        orm_mode = True
