from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.comments import CommentBase, CommentModel


async def create_comment(db: Session, comment_data: dict, user_id: int, photo_id: int):
    comment = Comment(**comment_data, user_id=user_id, photo_id=photo_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
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
