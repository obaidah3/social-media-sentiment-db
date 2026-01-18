# app/v1/stories.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Story
from app.schemas.stories import StoryCreate, StoryResponse, StoryAuthor, StoriesListResponse
from app.api.deps import get_current_active_user, get_optional_user
from app.utils.file_handler import file_handler
from app.config import settings

router = APIRouter()

# Story table to track views (in-memory for now, should be in DB)
story_views = {}  # {story_id: [user_id1, user_id2, ...]}


@router.post("", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def create_story(
        media_type: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Create a new story (24-hour expiry)

    - **media_type**: 'image' or 'video'
    - **file**: Media file to upload

    Stories automatically expire after 24 hours
    """

    # Validate media type
    if media_type not in ['image', 'video']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Media type must be 'image' or 'video'"
        )

    # Upload media
    if media_type == 'image':
        media_url, file_path = await file_handler.save_image(file, 'stories')
    else:
        media_url, file_path = await file_handler.save_video(file, 'stories')

    # Calculate expiry time (24 hours from now)
    created_at = datetime.utcnow()
    expired_at = created_at + timedelta(hours=24)

    # Create story
    new_story = Story(
        user_id=current_user.User_id,
        Media_Url=media_url,
        MediaType=media_type,
        Created_at=created_at,
        Expired_at=expired_at
    )

    db.add(new_story)
    db.commit()
    db.refresh(new_story)

    # Build response
    author = StoryAuthor(
        User_id=current_user.User_id,
        Username=current_user.Username,
        Profile_pic_url=current_user.Profile_pic_url
    )

    return StoryResponse(
        Story_id=new_story.Story_id,
        user_id=new_story.user_id,
        author=author,
        Media_Url=new_story.Media_Url,
        MediaType=new_story.MediaType,
        Created_at=new_story.Created_at,
        Expired_at=new_story.Expired_at,
        is_expired=False,
        views_count=0,
        is_viewed=False
    )


@router.get("", response_model=StoriesListResponse)
def get_active_stories(
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Get all active (non-expired) stories from followed users

    Stories are grouped by user and ordered by recency
    """

    # Get current time
    now = datetime.utcnow()

    # Get stories from followed users + own stories
    if current_user:
        followed_ids = [u.User_id for u in current_user.following]
        followed_ids.append(current_user.User_id)

        stories = db.query(Story).filter(
            and_(
                Story.user_id.in_(followed_ids),
                Story.Expired_at > now
            )
        ).order_by(desc(Story.Created_at)).all()
    else:
        # Public stories (for non-authenticated users)
        stories = db.query(Story).filter(
            Story.Expired_at > now
        ).order_by(desc(Story.Created_at)).limit(50).all()

    # Build response
    stories_response = []
    has_unviewed = False

    for story in stories:
        # Check if expired
        is_expired = story.Expired_at <= now

        # Get views count
        views_count = len(story_views.get(story.Story_id, []))

        # Check if current user viewed
        is_viewed = False
        if current_user:
            is_viewed = current_user.User_id in story_views.get(story.Story_id, [])
            if not is_viewed:
                has_unviewed = True

        # Get author
        author = StoryAuthor(
            User_id=story.author.User_id,
            Username=story.author.Username,
            Profile_pic_url=story.author.Profile_pic_url
        )

        stories_response.append(StoryResponse(
            Story_id=story.Story_id,
            user_id=story.user_id,
            author=author,
            Media_Url=story.Media_Url,
            MediaType=story.MediaType,
            Created_at=story.Created_at,
            Expired_at=story.Expired_at,
            is_expired=is_expired,
            views_count=views_count,
            is_viewed=is_viewed
        ))

    return StoriesListResponse(
        stories=stories_response,
        total=len(stories_response),
        has_unviewed=has_unviewed
    )


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(
        story_id: int,
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_optional_user)
):
    """Get a specific story by ID"""

    story = db.query(Story).filter(Story.Story_id == story_id).first()

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )

    # Check if expired
    now = datetime.utcnow()
    is_expired = story.Expired_at <= now

    # Get views
    views_count = len(story_views.get(story_id, []))
    is_viewed = False
    if current_user:
        is_viewed = current_user.User_id in story_views.get(story_id, [])

    # Get author
    author = StoryAuthor(
        User_id=story.author.User_id,
        Username=story.author.Username,
        Profile_pic_url=story.author.Profile_pic_url
    )

    return StoryResponse(
        Story_id=story.Story_id,
        user_id=story.user_id,
        author=author,
        Media_Url=story.Media_Url,
        MediaType=story.MediaType,
        Created_at=story.Created_at,
        Expired_at=story.Expired_at,
        is_expired=is_expired,
        views_count=views_count,
        is_viewed=is_viewed
    )


@router.post("/{story_id}/view")
def mark_story_viewed(
        story_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Mark a story as viewed by current user

    This increments the view count and marks the story as seen
    """

    story = db.query(Story).filter(Story.Story_id == story_id).first()

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )

    # Add user to viewers list
    if story_id not in story_views:
        story_views[story_id] = []

    if current_user.User_id not in story_views[story_id]:
        story_views[story_id].append(current_user.User_id)

    return {
        "message": "Story marked as viewed",
        "views_count": len(story_views[story_id])
    }


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(
        story_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Delete a story. Only the author can delete their story.
    """

    story = db.query(Story).filter(Story.Story_id == story_id).first()

    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )

    # Check ownership
    if story.user_id != current_user.User_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own stories"
        )

    # Delete media file
    file_path = settings.UPLOAD_DIR + story.Media_Url.replace('/uploads', '')
    file_handler.delete_file(file_path)

    # Delete from views tracking
    if story_id in story_views:
        del story_views[story_id]

    # Delete story
    db.delete(story)
    db.commit()

    return None


@router.get("/user/{user_id}", response_model=List[StoryResponse])
def get_user_stories(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Get all active stories from a specific user
    """

    # Verify user exists
    user = db.query(User).filter(User.User_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get active stories
    now = datetime.utcnow()
    stories = db.query(Story).filter(
        and_(
            Story.user_id == user_id,
            Story.Expired_at > now
        )
    ).order_by(desc(Story.Created_at)).all()

    # Build response
    stories_response = []
    for story in stories:
        is_expired = story.Expired_at <= now
        views_count = len(story_views.get(story.Story_id, []))
        is_viewed = False
        if current_user:
            is_viewed = current_user.User_id in story_views.get(story.Story_id, [])

        author = StoryAuthor(
            User_id=user.User_id,
            Username=user.Username,
            Profile_pic_url=user.Profile_pic_url
        )

        stories_response.append(StoryResponse(
            Story_id=story.Story_id,
            user_id=story.user_id,
            author=author,
            Media_Url=story.Media_Url,
            MediaType=story.MediaType,
            Created_at=story.Created_at,
            Expired_at=story.Expired_at,
            is_expired=is_expired,
            views_count=views_count,
            is_viewed=is_viewed
        ))

    return stories_response