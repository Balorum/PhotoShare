from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.comments import CommentBase, CommentModel


async def show_comment() -> Comment | None:
    pass


async def create_comment(
    db: Session, comment: CommentBase, user_id: int, photo_id: int
) -> Comment:
    db_comment = Comment(comment, user_id=user_id, post_id=photo_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def edit_comment() -> Comment | None:
    pass


async def delete_comment() -> None:
    pass
