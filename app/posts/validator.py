from typing import List, ClassVar, Optional
from fastapi import Query, HTTPException
from pydantic import BaseModel, field_validator


class IncludeQueryParams(BaseModel):
    include: List[str]
    valid_include_fields: ClassVar[Optional[set]] = None

    @field_validator("include")
    def split_and_validate(cls, value):
        if cls.valid_include_fields is None:
            raise ValueError("valid_include_fields must be set")
        if isinstance(value, str):
            value = value.split(",")
        invalid = set(value) - cls.valid_include_fields
        if invalid:
            raise ValueError(f"Invalid include values: {invalid}")
        return value


def validate_against(valid_include_fields):
    valid_set = set(valid_include_fields)

    class DynamicIncludeParams(IncludeQueryParams):
        valid_include_fields: ClassVar[set] = valid_set

    def get_include_params(
        include: str = Query(
            "", description="Comma-separated list of fields to include"
        )
    ):
        try:
            return DynamicIncludeParams(
                include=include.split(",") if include else []
            ).include
        except ValueError as e:
            raise HTTPException(400, detail=str(e.errors()[0]["msg"]))

    return get_include_params
