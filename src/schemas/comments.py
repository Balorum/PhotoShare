from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: str


class CommentModel(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
