from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    pass


class TagModel(TagBase):
    pass


class TagResponse(TagBase):
    pass


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
