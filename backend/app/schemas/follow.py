from pydantic import BaseModel
from datetime import datetime


class FollowResponse(BaseModel):
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FollowUser(BaseModel):
    id: int
    username: str
    profile_pic_url: str | None = None

    class Config:
        orm_mode = True
