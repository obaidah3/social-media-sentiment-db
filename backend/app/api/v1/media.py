# app/v1/media.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import User, Post, Media
from app.schemas.posts import MediaResponse
from app.api.deps import get_current_active_user
from app.utils.file_handler import file_handler
from app.config import settings

router = APIRouter()


@router.post("/upload", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(
        file: UploadFile = File(...),
        media_type: str = "image",
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Upload a media file (image or video)

    - **file**: Media file to upload
    - **media_type**: 'image' or 'video'

    Returns media object that can be attached to posts
    """

    # Validate media type
    if media_type not in ['image', 'video']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Media type must be 'image' or 'video'"
        )

    # Upload file
    if media_type == 'image':
        media_url, file_path = await file_handler.save_image(file, 'posts')
    else:
        media_url, file_path = await file_handler.save_video(file, 'posts')

    # Create media record
    new_media = Media(
        Media_type=media_type,
        Media_url=media_url,
        Uploaded_at=datetime.utcnow()
    )

    db.add(new_media)
    db.commit()
    db.refresh(new_media)

    return MediaResponse(
        Media_id=new_media.Media_id,
        Media_type=new_media.Media_type,
        Media_url=new_media.Media_url,
        Uploaded_at=new_media.Uploaded_at
    )


@router.post("/posts/{post_id}/attach")
def attach_media_to_post(
        post_id: int,
        media_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Attach uploaded media to a post

    - **post_id**: ID of the post
    - **media_ids**: List of media IDs to attach
    """

    # Get post
    post = db.query(Post).filter(Post.post_id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check ownership
    if post.user_id != current_user.User_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only attach media to your own posts"
        )

    # Get media objects
    media_objects = db.query(Media).filter(Media.Media_id.in_(media_ids)).all()

    if len(media_objects) != len(media_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more media items not found"
        )

    # Attach media to post
    for media in media_objects:
        if media not in post.media:
            post.media.append(media)

    db.commit()

    return {
        "message": "Media attached successfully",
        "post_id": post_id,
        "media_count": len(post.media)
    }


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
        media_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Delete a media file

    Note: This will remove the media from all posts it's attached to
    """

    media = db.query(Media).filter(Media.Media_id == media_id).first()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    # Delete file from disk
    file_path = settings.UPLOAD_DIR + media.Media_url.replace('/uploads', '')
    file_handler.delete_file(file_path)

    # Delete from database
    db.delete(media)
    db.commit()

    return None


@router.get("/{media_id}", response_model=MediaResponse)
def get_media(
        media_id: int,
        db: Session = Depends(get_db)
):
    """Get media information by ID"""

    media = db.query(Media).filter(Media.Media_id == media_id).first()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    return MediaResponse(
        Media_id=media.Media_id,
        Media_type=media.Media_type,
        Media_url=media.Media_url,
        Uploaded_at=media.Uploaded_at
    )