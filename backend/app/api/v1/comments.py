from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models import Comment, Post, Sentiment, User
from app.schemas.comments import CommentCreate, CommentResponse, CommentAuthor
from app.api.deps import get_current_active_user
from app.utils.sentiment import analyze_sentiment
from app.services.notifications import create_notification

router = APIRouter(prefix="/comments", tags=["Comments"])


# =========================================================
# Helpers
# =========================================================

def build_comment_response(comment: Comment) -> CommentResponse:
    """
    Builds a comment response with ONE LEVEL of replies only
    (prevents infinite recursion)
    """
    return CommentResponse(
        id=comment.id,
        post_id=comment.post_id,
        content=comment.content,
        created_at=comment.created_at,
        author=CommentAuthor(
            id=comment.user.id,
            username=comment.user.username,
            profile_pic_url=getattr(comment.user.profile, "profile_pic_url", None)
        ),
        replies=[
            CommentResponse(
                id=reply.id,
                post_id=reply.post_id,
                content=reply.content,
                created_at=reply.created_at,
                author=CommentAuthor(
                    id=reply.user.id,
                    username=reply.user.username,
                    profile_pic_url=getattr(reply.user.profile, "profile_pic_url", None)
                ),
                replies=[]  # ⛔ stop recursion here
            )
            for reply in comment.replies
        ]
    )


# =========================================================
# Create Comment
# =========================================================

@router.post(
    "/posts/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if data.parent_id:
        parent = db.query(Comment).filter(
            Comment.id == data.parent_id,
            Comment.post_id == post_id
        ).first()
        if not parent:
            raise HTTPException(
                status_code=400,
                detail="Invalid parent comment"
            )

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=data.content,
        parent_id=data.parent_id
    )

    db.add(comment)
    db.flush()

    sentiment_result = analyze_sentiment(data.content)

    db.add(Sentiment(
        comment_id=comment.id,
        label=sentiment_result["label"],
        score=sentiment_result["score"],
        target_type="comment"
    ))

    if post.user_id != current_user.id:
        create_notification(
            db=db,
            recipient_id=post.user_id,
            actor_id=current_user.id,
            type="comment",
            object_id=post.id,
            object_type="post"
        )

    db.commit()
    db.refresh(comment)

    return build_comment_response(comment)


# =========================================================
# List Comments
# =========================================================

@router.get(
    "/posts/{post_id}",
    response_model=List[CommentResponse]
)
def list_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    comments = (
        db.query(Comment)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.replies).selectinload(Comment.user)
        )
        .filter(
            Comment.post_id == post_id,
            Comment.parent_id.is_(None)
        )
        .order_by(Comment.created_at.asc())
        .all()
    )

    return [build_comment_response(c) for c in comments]


# =========================================================
# Delete Comment
# =========================================================

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Explicit sentiment cleanup (safe for DB project)
    db.query(Sentiment).filter(
        Sentiment.comment_id == comment.id
    ).delete()

    db.delete(comment)
    db.commit()

    return None
