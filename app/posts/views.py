from typing import List
from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.posts.models import Post as PostModel, User as UserModel
from app.posts.constants import PostStatus
from app.posts.validator import validate_against
from app.posts.cached_schema_factory import CachedSchemaFactory
from loguru import logger


router = APIRouter()


@router.get("/posts", status_code=200)
async def get_posts(
    status: PostStatus | None = Query(
        None,
        description="Filter posts by status",
        examples=["draft", "public", "private"],
    ),
    include: List[str] = Depends(validate_against(["tags", "comments", "user"])),
    db: Session = Depends(get_db),
):
    """
    Get all posts with optional status filtering

    Parameters:
    - status: Filter posts by status (draft, public, private)
    - include: Include nested objects by name (comments, tags, user)

    Returns:
    - list: An array of post objects
    """

    query = db.query(PostModel)

    if status:
        query = query.filter(PostModel.status == status)

    factory = CachedSchemaFactory(PostModel, include)
    schema = factory.get_or_create_class()
    return [schema.model_validate(item).model_dump() for item in query]


@router.get("/posts/{post_id}", status_code=200)
async def get_post(
    post_id: int,
    include: List[str] = Depends(validate_against(["tags", "comments", "user"])),
    db: Session = Depends(get_db),
):
    """
    Get a single post.

    Parameters:
    - include: Include nested objects by name (comments, tags, user)

    Returns:
    - Post object
    """

    query = db.query(PostModel).filter(PostModel.id == post_id).first()

    if not query:
        desc = "Post not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    factory = CachedSchemaFactory(PostModel, include)
    schema = factory.get_or_create_class()
    return schema.model_validate(query).model_dump()


@router.get("/users/{user_id}", status_code=200)
async def get_users(
    user_id: int,
    include: List[str] = Depends(validate_against(["posts", "comments"])),
    db: Session = Depends(get_db),
):
    """
    Get all users

    Parameters:
    - include: Include nested objects by name (comments, tags, posts)

    Returns:
    - list: An array of user objects
    """

    query = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not query:
        desc = "User not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    factory = CachedSchemaFactory(UserModel, include)
    schema = factory.get_or_create_class()
    return schema.model_validate(query).model_dump()
