from pydantic import BaseModel, Field
from schemas.user import UserSchema


class PostSchema(BaseModel):
    title: str = Field(max_length=40)
    content: str


class PostDbSchema(PostSchema):
    post_id: str
    author: UserSchema
    image: str | None = Field(default=None, max_length=80)


class PostOutSchema(PostDbSchema):
    pass
