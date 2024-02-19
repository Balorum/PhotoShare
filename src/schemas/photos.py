from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    title: str = Field(max_length=50)


class TagModel(TagBase):
    pass

    class Config:
            orm_mode = True


class TagResponse(TagBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    pass


class CommentModel(CommentBase):
    pass


class CommentUpdate(CommentModel):
    pass


class PhotoBase(BaseModel):
    pass


class PhotoModel(PhotoBase):
    pass


class PhotoUpdate(BaseModel):
    pass

class PhotoStatusUpdate(BaseModel):
    pass

class PhotoResponse(PhotoBase):
    pass


class RequestRole(BaseModel):
    pass
