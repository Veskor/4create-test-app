from enum import Enum


class PostStatus(str, Enum):
    draft = "draft"
    public = "public"
    private = "private"
