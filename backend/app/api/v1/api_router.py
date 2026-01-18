from fastapi import APIRouter

from app.api.v1 import (
    auth,
    users,
    posts,
    profiles,
    comments,
    follows,
    notifications
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(follows.router, prefix="/follows", tags=["Follows"])
api_router.include_router(comments.router)
api_router.include_router(notifications.router,prefix="/notifications",tags=["Notifications"]
)
