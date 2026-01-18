# # app/v1/__init__.py
# from fastapi import APIRouter
# from app.api.v1 import auth, users, posts, profiles, follows, bookmarks
# from app.api.v1 import feed
# from app.api.v1 import follows
# from app.api.v1.api_router import api_router
#
# # api_router = APIRouter()
#
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
# api_router.include_router(feed.router, prefix="/feed", tags=["Feed"])
# api_router.include_router(follows.router, prefix="/follows", tags=["Follows"])
# api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["Bookmarks"])

from app.api.v1.api_router import api_router
