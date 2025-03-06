from typing import List
from typing import Optional
from app.posts.constants import PostStatus
from app.posts.models import User as UserModel, Post as PostModel
from app.posts.schema import (
    Post as PostSchema,
    Tag as TagSchema,
    User as UserSchema,
    Comment as CommentSchema,
)
from pydantic import create_model, ConfigDict
from copy import deepcopy


class CachedSchemaFactory:
    schema_class_cache = {}
    base_field_sets = {
        UserModel: {
            "id": (int, ...),
            "name": (str, ...),
        },
        PostModel: {
            "id": (int, ...),
            "content": (str, ...),
            "title": (str, ...),
            "status": (PostStatus, ...),
        },
    }
    schema_extensions = {
        "posts": (Optional[List[PostSchema]], None),
        "comments": (Optional[List[CommentSchema]], None),
        "tags": (Optional[List[TagSchema]], None),
        "user": (Optional[UserSchema], None),
    }

    def __init__(self, model_class, attributes):
        self.model_class = model_class
        self.attributes = attributes
        self.base_fields = self.base_field_sets[self.model_class]

    @property
    def cache_key(self):
        return (self.model_class.__name__, tuple(sorted(set(self.attributes))))

    def get_or_create_class(self):

        if self.cache_key in self.schema_class_cache:
            return self.schema_class_cache[self.cache_key]

        fields = deepcopy(self.base_fields)
        for attribute in self.attributes:
            fields.update({attribute: self.schema_extensions[attribute]})

        dynamic_model = create_model(
            "DynamicModel", **fields, __config__=ConfigDict(from_attributes=True)
        )
        self.schema_class_cache[self.cache_key] = dynamic_model

        return dynamic_model
