from sqlalchemy.orm import Session
from typing import Optional

from app.models import Notification


def create_notification(
    *,
    db: Session,
    recipient_id: int,
    actor_id: int,
    type: str,
    object_id: Optional[int] = None,
    object_type: Optional[str] = None
) -> Optional[Notification]:
    """
    Create a notification safely.
    The caller controls the transaction (commit/rollback).
    """

    # =========================
    # Validation
    # =========================

    if not recipient_id or not actor_id:
        return None

    # Do not notify yourself
    if recipient_id == actor_id:
        return None

    # =========================
    # Create notification
    # =========================

    notification = Notification(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=type,
        object_id=object_id,
        object_type=object_type
    )

    db.add(notification)
    db.flush()  # ensures ID exists if needed immediately

    return notification
