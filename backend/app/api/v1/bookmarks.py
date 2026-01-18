from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload
from typing import Optional

from app.database import get_db
from app.models import Bookmark, Post, User
from app.api.deps import get_current_active_user
from app.api.v1.posts import build_post_response

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


# =========================================================
# Toggle Bookmark (Save / Unsave)
# =========================================================

@router.post("/{post_id}", status_code=status.HTTP_200_OK)
def toggle_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.post_id == post_id
    ).first()

    # Unsave
    if bookmark:
        db.delete(bookmark)
        db.commit()
        return {"saved": False}

    # Save
    db.add(
        Bookmark(
            user_id=current_user.id,
            post_id=post_id
        )
    )
    db.commit()

    return {"saved": True}


# =========================================================
# Get My Bookmarked Posts
# =========================================================

@router.get("", status_code=status.HTTP_200_OK)
def get_my_bookmarks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    offset = (page - 1) * page_size

    query = (
        db.query(Bookmark)
        .options(
            selectinload(Bookmark.post)
            .selectinload(Post.user)
        )
        .filter(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at.desc())
    )

    total = query.count()

    bookmarks = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    posts = [
        build_post_response(b.post, db, current_user)
        for b in bookmarks
    ]

    return {
        "posts": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": (offset + page_size) < total
    }
