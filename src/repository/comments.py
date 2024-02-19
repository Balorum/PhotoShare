from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.photos import CommentBase


async def show_comment(db: Session, comment_id: int) -> Optional[Comment]:
    return await db.query(Comment).filter(Comment.id == comment_id).first()


async def create_comment(
    db: Session, comment: CommentBase, user_id: int, photo_id: int
) -> Comment:
    db_comment = Comment(**comment.dict(), user_id=user_id, post_id=photo_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def edit_comment(
    db: Session, comment_id: int, new_text: str
) -> Optional[Comment]:
    comment = await db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        comment.text = new_text
        await db.commit()
        await db.refresh(comment)
    return comment


async def delete_comment(db: Session, comment_id: int) -> None:
    comment = await db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        await db.commit()


async def get_comments_by_user(db: Session, user_id: int) -> List[Comment]:
    return await db.query(Comment).filter(Comment.user_id == user_id).all()


async def get_comments_by_post(db: Session, post_id: int) -> List[Comment]:
    return await db.query(Comment).filter(Comment.post_id == post_id).all()
