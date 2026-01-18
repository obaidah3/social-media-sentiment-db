# app/api/v1/feed.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Post, Follow, User
from app.schemas.posts import PostResponse
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=list[PostResponse])
def get_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    offset = (page - 1) * limit

    followed_subquery = (
        db.query(Follow.following_id)
        .filter(Follow.follower_id == current_user.id)
    )

    posts = (
        db.query(Post)
        .filter(
            or_(
                Post.user_id.in_(followed_subquery),
                Post.user_id == current_user.id
            )
        )
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return posts
