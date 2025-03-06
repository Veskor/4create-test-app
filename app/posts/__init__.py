from fastapi import APIRouter
from app.posts.views import router

API_STR = "/api"

posts_router = APIRouter(prefix=API_STR)
posts_router.include_router(router)
