from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from app.database import get_db
from app.models import User, Post, Reaction, Sentiment, Comment, Bookmark
from app.schemas.posts import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostAuthor,
    ReactionCreate,
    ReactionResponse,
    FeedResponse,
    SentimentAnalysis,
    MediaResponse
)
from app.api.deps import get_current_active_user, get_optional_user
from app.utils.sentiment import analyze_sentiment
from app.services.notifications import create_notification

router = APIRouter(tags=["Posts"])


# =========================================================
# Helpers
# =========================================================

def build_post_response(
    post: Post,
    db: Session,
    current_user: Optional[User] = None
) -> dict:
    likes_count = db.query(Reaction).filter(
        Reaction.post_id == post.id
    ).count()

    comments_count = db.query(Comment).filter(
        Comment.post_id == post.id
    ).count()

    sentiment = None
    if post.sentiment:
        sentiment = SentimentAnalysis(
            label=post.sentiment.label,
            score=float(post.sentiment.score),
            confidence=0.9,
            toxicity="none"
        )

    is_liked = False
    is_saved = False

    if current_user:
        is_liked = db.query(Reaction).filter(
            Reaction.user_id == current_user.id,
            Reaction.post_id == post.id
        ).first() is not None

        is_saved = db.query(Bookmark).filter(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post.id
        ).first() is not None

    media = [MediaResponse.from_orm(m) for m in post.media]

    author = PostAuthor(
        id=post.user.id,
        username=post.user.username,
        profile_pic_url=getattr(post.user.profile, "profile_pic_url", None)
    )

    return {
        "id": post.id,
        "user_id": post.user_id,
        "author": author,
        "content": post.content,
        "visibility": post.visibility,
        "location": post.location,
        "platform": post.platform,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "likes_count": likes_count,
        "comments_count": comments_count,
        "shares_count": 0,
        "sentiment": sentiment,
        "media": media,
        "is_liked": is_liked,
        "is_saved": is_saved
    }


# =========================================================
# Create Post
# =========================================================

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    sentiment_result = analyze_sentiment(post_data.content)

    post = Post(
        user_id=current_user.id,
        content=post_data.content,
        visibility=post_data.visibility or "public"
    )

    db.add(post)
    db.flush()

    db.add(Sentiment(
        post_id=post.id,
        label=sentiment_result["label"],
        score=sentiment_result["score"],
        target_type="post"
    ))

    db.commit()
    db.refresh(post)

    return build_post_response(post, db, current_user)


# =========================================================
# Feed
# =========================================================

@router.get("/feed", response_model=FeedResponse)
def get_feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    offset = (page - 1) * page_size

    query = (
        db.query(Post)
        .filter(Post.visibility == "public")
        .order_by(desc(Post.created_at))
    )

    total = query.count()
    posts = query.offset(offset).limit(page_size).all()

    return FeedResponse(
        posts=[build_post_response(p, db, current_user) for p in posts],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(offset + page_size) < total
    )


# =========================================================
# Get Single Post
# =========================================================

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.visibility != "public":
        if not current_user or post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

    return build_post_response(post, db, current_user)


# =========================================================
# Update Post
# =========================================================

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if post_update.content:
        post.content = post_update.content
        sentiment_result = analyze_sentiment(post_update.content)

        if post.sentiment:
            post.sentiment.label = sentiment_result["label"]
            post.sentiment.score = sentiment_result["score"]
        else:
            db.add(Sentiment(
                post_id=post.id,
                label=sentiment_result["label"],
                score=sentiment_result["score"],
                target_type="post"
            ))

    if post_update.visibility:
        post.visibility = post_update.visibility

    db.commit()
    db.refresh(post)

    return build_post_response(post, db, current_user)


# =========================================================
# Reactions
# =========================================================

@router.post("/{post_id}/react", response_model=ReactionResponse)
def toggle_reaction(
    post_id: int,
    reaction_data: ReactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    reaction = db.query(Reaction).filter(
        Reaction.user_id == current_user.id,
        Reaction.post_id == post_id
    ).first()

    if reaction:
        if reaction.reaction_type == reaction_data.reaction_type:
            db.delete(reaction)
        else:
            reaction.reaction_type = reaction_data.reaction_type
    else:
        db.add(Reaction(
            user_id=current_user.id,
            post_id=post_id,
            reaction_type=reaction_data.reaction_type
        ))

        create_notification(
            db=db,
            recipient_id=post.user_id,
            actor_id=current_user.id,
            type="like",
            object_id=post_id,
            object_type="post"
        )

    db.commit()

    reactions = db.query(Reaction).filter(
        Reaction.post_id == post_id
    ).all()

    breakdown = {}
    for r in reactions:
        breakdown[r.reaction_type] = breakdown.get(r.reaction_type, 0) + 1

    user_reaction = db.query(Reaction).filter(
        Reaction.user_id == current_user.id,
        Reaction.post_id == post_id
    ).first()

    return ReactionResponse(
        total=len(reactions),
        breakdown=breakdown,
        user_reaction=user_reaction.reaction_type if user_reaction else None
    )


# =========================================================
# Trending
# =========================================================

@router.get("/trending", response_model=FeedResponse)
def trending_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    offset = (page - 1) * page_size

    posts = db.query(Post).filter(
        Post.visibility == "public"
    ).all()

    scored = []
    for post in posts:
        likes = db.query(Reaction).filter(
            Reaction.post_id == post.id
        ).count()

        comments = db.query(Comment).filter(
            Comment.post_id == post.id
        ).count()

        scored.append((post, likes + comments * 2))

    scored.sort(key=lambda x: x[1], reverse=True)

    paginated = scored[offset: offset + page_size]
    result_posts = [p[0] for p in paginated]

    return FeedResponse(
        posts=[build_post_response(p, db, current_user) for p in result_posts],
        total=len(scored),
        page=page,
        page_size=page_size,
        has_more=(offset + page_size) < len(scored)
    )

# =========================================================
# Get Posts By User (Profile)
# =========================================================

@router.get("/user/{user_id}", response_model=FeedResponse)
def get_posts_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(desc(Post.created_at))
        .all()
    )

    return FeedResponse(
        posts=[build_post_response(p, db, current_user) for p in posts],
        total=len(posts),
        page=1,
        page_size=len(posts),
        has_more=False
    )
