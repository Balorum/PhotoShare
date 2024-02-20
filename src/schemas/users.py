from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role, User


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=16)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserUpdateModel(BaseModel):
    pass


class RequestEmail(BaseModel):
    email: EmailStr
