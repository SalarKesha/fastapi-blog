from pydantic import BaseModel, Field
from bson import ObjectId


class BaseUserSchema(BaseModel):
    username: str = Field(max_length=40)


class UserSchema(BaseUserSchema):
    user_id: str


class UserDbSchema(UserSchema):
    password: str


class UserCreateSchema(BaseUserSchema):
    password: str
