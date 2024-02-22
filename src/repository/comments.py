from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.comments import CommentBase, CommentModel, CommentUpdate


async def create_comment(
    db: Session, comment_data: CommentModel, photo_id: int, user_id: int
):
    comment = Comment(
        text=comment_data.get("text"),
        created_at=comment_data.get("created_at"),
        updated_at=comment_data.get("updated_at"),
        user_id=user_id,
        photo_id=photo_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


async def edit_comment(db: Session, comment_id: int, new_text: str):
    comment = await get_comment(db, comment_id)
    if comment:
        comment.text = new_text
        await db.commit()
        await db.refresh(comment)
    return comment


async def delete_comment(db: Session, comment_id: int):
    comment = await get_comment(db, comment_id)
    if comment:
        db.delete(comment)
        await db.commit()
    return comment
