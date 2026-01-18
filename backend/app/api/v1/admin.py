# app/v1/admin.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List, Optional
from datetime import date, datetime, timedelta

from app.database import get_db
from app.models import User, Post, Comment, Sentiment
from app.schemas.admin import (
    ModerationAction, FlaggedContent, UserManagement,
    SystemStats, UserDetail
)
from app.api.deps import get_current_active_user

router = APIRouter()


def verify_admin(current_user: User):
    """Verify user has admin privileges"""
    # Check role field (added in fixed User model)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


@router.get("/stats", response_model=SystemStats)
def get_system_stats(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get system-wide statistics - Requires admin privileges"""
    verify_admin(current_user)

    today = date.today()

    total_users = db.query(User).count()
    active_users_today = db.query(func.count(func.distinct(Post.user_id))).filter(
        Post.Post_date == today
    ).scalar() or 0

    total_posts = db.query(Post).count()
    posts_today = db.query(Post).filter(Post.Post_date == today).count()

    total_comments = db.query(Comment).count()
    comments_today = db.query(Comment).filter(Comment.Comment_date == today).count()

    flagged_content = db.query(Sentiment).filter(
        Sentiment.Sentiment_Label == 'negative'
    ).count()

    suspended_users = db.query(User).filter(User.status == 'suspended').count()

    return SystemStats(
        total_users=total_users,
        active_users_today=active_users_today,
        total_posts=total_posts,
        posts_today=posts_today,
        total_comments=total_comments,
        comments_today=comments_today,
        flagged_content_count=flagged_content,
        suspended_users_count=suspended_users
    )


@router.get("/flagged-content", response_model=List[FlaggedContent])
def get_flagged_content(
        content_type: Optional[str] = Query(None, pattern="^(post|comment|all)$"),
        limit: int = Query(50, ge=1, le=200),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get flagged content for moderation"""
    verify_admin(current_user)

    flagged_items = []

    if content_type in [None, 'all', 'post']:
        toxic_posts = db.query(Post, Sentiment, User).join(
            Sentiment, Sentiment.Post_Id == Post.post_id
        ).join(
            User, User.User_id == Post.user_id
        ).filter(
            Sentiment.Sentiment_Label == 'negative'
        ).order_by(desc(Post.Post_date)).limit(limit).all()

        for post, sentiment, user in toxic_posts:
            flagged_items.append(FlaggedContent(
                content_id=post.post_id,
                content_type='post',
                content_text=post.Content[:200] + '...' if len(post.Content) > 200 else post.Content,
                author_id=user.User_id,
                author_username=user.Username,
                sentiment_label=sentiment.Sentiment_Label,
                toxicity_level='high',
                flag_count=1,
                created_at=datetime.combine(post.Post_date, datetime.min.time())
            ))

    if content_type in [None, 'all', 'comment']:
        toxic_comments = db.query(Comment, Sentiment, User).join(
            Sentiment, Sentiment.comment_id == Comment.Comment_id
        ).join(
            User, User.User_id == Comment.User_id
        ).filter(
            Sentiment.Sentiment_Label == 'negative'
        ).order_by(desc(Comment.Comment_date)).limit(limit).all()

        for comment, sentiment, user in toxic_comments:
            flagged_items.append(FlaggedContent(
                content_id=comment.Comment_id,
                content_type='comment',
                content_text=comment.Comment_Text[:200] + '...' if len(
                    comment.Comment_Text) > 200 else comment.Comment_Text,
                author_id=user.User_id,
                author_username=user.Username,
                sentiment_label=sentiment.Sentiment_Label,
                toxicity_level='medium',
                flag_count=1,
                created_at=datetime.combine(comment.Comment_date, datetime.min.time())
            ))

    flagged_items.sort(key=lambda x: x.created_at, reverse=True)
    return flagged_items[:limit]


@router.post("/moderate/{content_type}/{content_id}")
def moderate_content(
        content_type: str,
        content_id: int,
        action_data: ModerationAction,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Take moderation action on content"""
    verify_admin(current_user)

    if content_type == 'post':
        content = db.query(Post).filter(Post.post_id == content_id).first()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        author_id = content.user_id
    elif content_type == 'comment':
        content = db.query(Comment).filter(Comment.Comment_id == content_id).first()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        author_id = content.User_id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content type"
        )

    if action_data.action == 'remove':
        db.delete(content)
        db.commit()
        message = f"{content_type.capitalize()} removed successfully"

    elif action_data.action == 'approve':
        message = f"{content_type.capitalize()} approved"

    elif action_data.action == 'suspend_user':
        user = db.query(User).filter(User.User_id == author_id).first()
        if user:
            user.status = 'suspended'
            db.commit()
        message = f"User suspended"

    elif action_data.action == 'warn':
        message = f"Warning sent to user"

    return {
        "message": message,
        "content_type": content_type,
        "content_id": content_id,
        "action": action_data.action,
        "reason": action_data.reason
    }


@router.get("/users", response_model=List[UserDetail])
def get_all_users(
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
        search: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get all users with detailed information"""
    verify_admin(current_user)

    offset = (page - 1) * page_size

    query = db.query(User)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.Username.ilike(search_term)) | (User.Email.ilike(search_term))
        )

    users = query.offset(offset).limit(page_size).all()

    users_detail = []
    for user in users:
        posts_count = db.query(Post).filter(Post.user_id == user.User_id).count()
        comments_count = db.query(Comment).filter(Comment.User_id == user.User_id).count()

        users_detail.append(UserDetail(
            User_id=user.User_id,
            Username=user.Username,
            Email=user.Email,
            Date_Joined=user.Date_Joined,
            Country=user.Country,
            role=user.role,
            status=user.status,
            posts_count=posts_count,
            comments_count=comments_count,
            followers_count=user.followers_count,
            following_count=user.following_count,
            flags_received=0
        ))

    return users_detail


@router.post("/users/{user_id}/manage")
def manage_user(
        user_id: int,
        action_data: UserManagement,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Manage user account"""
    verify_admin(current_user)

    user = db.query(User).filter(User.User_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_id == current_user.User_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot manage your own account"
        )

    if action_data.action == 'delete':
        db.delete(user)
        db.commit()
        message = "User deleted successfully"

    elif action_data.action == 'suspend':
        user.status = 'suspended'
        db.commit()
        message = "User suspended"

    elif action_data.action == 'unsuspend':
        user.status = 'active'
        db.commit()
        message = "User unsuspended"

    elif action_data.action == 'make_admin':
        user.role = 'admin'
        db.commit()
        message = "User promoted to admin"

    elif action_data.action == 'remove_admin':
        user.role = 'user'
        db.commit()
        message = "Admin privileges removed"

    return {
        "message": message,
        "user_id": user_id,
        "action": action_data.action,
        "reason": action_data.reason
    }


@router.get("/activity-log")
def get_activity_log(
        days: int = Query(7, ge=1, le=90),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get system activity log"""
    verify_admin(current_user)

    start_date = date.today() - timedelta(days=days)

    daily_stats = []

    for i in range(days):
        check_date = start_date + timedelta(days=i)

        posts_count = db.query(Post).filter(Post.Post_date == check_date).count()
        comments_count = db.query(Comment).filter(Comment.Comment_date == check_date).count()
        new_users = db.query(User).filter(User.Date_Joined == check_date).count()

        daily_stats.append({
            "date": check_date.isoformat(),
            "posts": posts_count,
            "comments": comments_count,
            "new_users": new_users
        })

    return {
        "period_days": days,
        "daily_activity": daily_stats
    }