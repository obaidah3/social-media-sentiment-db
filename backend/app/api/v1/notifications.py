from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Notification, User
from app.schemas.notifications import NotificationResponse, NotificationActor
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationResponse])
def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    offset = (page - 1) * page_size

    notifications = (
        db.query(Notification)
        .filter(Notification.recipient_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return [
        NotificationResponse(
            id=n.id,
            type=n.type,
            object_id=n.object_id,
            object_type=n.object_type,
            is_read=n.is_read,
            created_at=n.created_at,
            actor=NotificationActor(
                id=n.actor.id,
                username=n.actor.username,
                profile_pic_url=getattr(
                    n.actor.profile, "profile_pic_url", None
                )
            )
        )
        for n in notifications
    ]

@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.recipient_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()

    return None

@router.patch("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.recipient_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()

    return None

@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    count = db.query(Notification).filter(
        Notification.recipient_id == current_user.id,
        Notification.is_read == False
    ).count()

    return {"unread": count}

