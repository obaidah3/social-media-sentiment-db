from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Follow
from app.schemas.follow import FollowResponse, FollowUser
from app.api.deps import get_current_active_user
from app.services.notifications import create_notification

router = APIRouter(prefix="/follows", tags=["Follows"])


# =========================================================
# Follow User
# =========================================================

@router.post("/{user_id}", response_model=FollowResponse)
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot follow yourself"
        )

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()

    # Idempotent follow
    if follow:
        return follow

    follow = Follow(
        follower_id=current_user.id,
        following_id=user_id
    )

    db.add(follow)

    create_notification(
        db=db,
        recipient_id=user_id,
        actor_id=current_user.id,
        type="follow",
        object_id=current_user.id,
        object_type="profile"
    )

    db.commit()
    db.refresh(follow)

    return follow



# =========================================================
# Unfollow User
# =========================================================

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()

    if not follow:
        raise HTTPException(
            status_code=404,
            detail="Not following this user"
        )

    db.delete(follow)
    db.commit()

    return None


# =========================================================
# Get Followers
# =========================================================

@router.get("/{user_id}/followers")
def get_followers(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    offset = (page - 1) * page_size

    query = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
    )

    total = query.count()

    users = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": (offset + page_size) < total,
        "users": [
            FollowUser(
                id=u.id,
                username=u.username,
                profile_pic_url=getattr(u.profile, "profile_pic_url", None)
            )
            for u in users
        ]
    }


# =========================================================
# Get Following
# =========================================================

@router.get("/{user_id}/following")
def get_following(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    offset = (page - 1) * page_size

    query = (
        db.query(User)
        .join(Follow, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
    )

    total = query.count()

    users = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": (offset + page_size) < total,
        "users": [
            FollowUser(
                id=u.id,
                username=u.username,
                profile_pic_url=getattr(u.profile, "profile_pic_url", None)
            )
            for u in users
        ]
    }

@router.get("/{user_id}/status")
def follow_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    is_following = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first() is not None

    return {"is_following": is_following}
