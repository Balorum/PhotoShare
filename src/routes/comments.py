from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.db import get_db
from src.database.models import User
from src.schemas.comments import CommentBase, CommentModel, CommentUpdate, CommentCreate
from src.repository import comments as repository_comments
from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/create/{photo_id}",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    photo_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_s),
):
    # Add creation timestamp
    print("////", db, "\\\\")
    now = datetime.now()
    comment_data = comment.dict()
    comment_data["created_at"] = now
    comment_data["updated_at"] = now
    result = await repository_comments.create_comment(
        db, comment_data, photo_id, current_user.id
    )
    return result


@router.put("/edit/{comment_id}", response_model=CommentUpdate)
async def edit_comment(
    comment_id: int,
    new_text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_s),
):
    comment = await repository_comments.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this comment",
        )
    updated_comment = await repository_comments.edit_comment(db, comment_id, new_text)
    # Update the timestamp
    updated_comment.updated_at = datetime.now()
    return updated_comment


@router.delete("/delete/{comment_id}", response_model=CommentModel)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_s),
):
    if not auth_service.is_admin_or_moderator(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and moderators can delete comments",
        )
    comment = await repository_comments.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    await repository_comments.delete_comment(db, comment_id)
    return comment
