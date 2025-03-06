from pydantic import BaseModel, ConfigDict
from app.posts.constants import PostStatus


class Post(BaseModel):
    title: str
    content: str
    status: PostStatus
    id: int

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    name: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class Comment(BaseModel):
    content: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class Tag(BaseModel):
    name: str
    id: int

    model_config = ConfigDict(from_attributes=True)
