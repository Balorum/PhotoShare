from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.photos import CommentBase


async def show_comment() -> Comment | None:
    pass


async def create_comment() -> Comment:
    pass


async def edit_comment() -> Comment | None:
    pass


async def delete_comment() -> None:
    pass


