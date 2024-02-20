from datetime import datetime

from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List



class TagModel(BaseModel):
    name: str = Field(max_length=20)

class TagBase(BaseModel):
    title: str = Field(max_length=50)


class PhotoBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    tags: List[str]

class TagResponse(TagBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PhotoResponse(PhotoBase):
    id: int
    created_at: datetime
    tags: List[TagResponse] | None


class CommentBase(BaseModel):
    pass


class CommentModel(CommentBase):
    pass


class CommentUpdate(CommentModel):
    pass


class RequestRole(BaseModel):
    pass
