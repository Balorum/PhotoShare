from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str


class CommentFind(CommentBase):
    photo_id: int


class CommentResponse(CommentBase):
    id: int
    text: str
    photo_id: int


class CommentUpdate(BaseModel):
    text: str


class CommentModel(BaseModel):
    text: str

    class Config:
        orm_mode = True
