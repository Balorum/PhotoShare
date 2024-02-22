from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    text: str


class CommentUpdate(BaseModel):
    text: str


class CommentModel(BaseModel):
    id: int
    text: str
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
