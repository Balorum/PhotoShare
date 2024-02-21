from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List

from src.database.models import User
from src.database.db import get_db
from src.schemas.photos import CommentBase, CommentUpdate, CommentModel
from src.repository import comments as repository_comments
from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/create/{photo_id}", response_model=CommentModel)
async def create_comment(
    photo_id: int,
    comment: CommentBase,
    db: Session = Depends(get_db),
):
    # current_user: User = Depends(auth_service.get_current_user)
    return await repository_comments.create_comment(db, comment, 1, photo_id)
    # db, comment, current_user.id, photo_id


@router.put("/edit/{comment_id}", response_model=CommentUpdate)
async def edit_comment(
    comment_id: int,
    new_text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    comment = await repository_comments.edit_comment(db, comment_id, new_text)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment updated successfully"}


@router.delete("/delete/{comment_id}", response_model=CommentModel)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    comment = await repository_comments.show_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to delete this comment"
        )
    await repository_comments.delete_comment(db, comment_id)
    return comment
