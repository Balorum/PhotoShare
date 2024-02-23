from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from src.database.db import get_db
from src.database.models import User
from src.schemas.comments import (
    CommentBase,
    CommentFind,
    CommentModel,
    CommentUpdate,
    CommentResponse,
)
from src.repository import comments as repository_comments
from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/create_comment/{photo_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    photo_id: int,
    comment: CommentModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_s),
):
    """
    The create_comment function creates a new comment for the image with the given ID.
        The user who created this comment is determined by the JWT token in the request header.

    :param photo_id: int: Get the photo that the comment is being made on
    :param comment: CommentModel: Create a new comment
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :param : Get the database session
    :return: A commentmodel object
    :doc-author: Trelent
    """
    return await repository_comments.create_comment(
        db,
        comment,
        photo_id,
        current_user.id,
    )


@router.put("/edit/{comment_id}", response_model=CommentUpdate)
async def edit_comment(
    comment_id: int,
    new_text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user_s),
):
    """
    The edit_comment function allows a user to edit their own comment.
        The function takes the comment_id and new_text as parameters, and returns the updated comment.


    :param comment_id: int: Identify the comment to be edited
    :param new_text: str: Pass in the new text for the comment
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is making the request
    :param : Get the comment id from the url
    :return: The updated comment object
    :doc-author: Trelent
    """
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
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_comment function deletes a comment from the database.
        Only admins and moderators can delete comments.


    :param comment_id: int: Get the comment id from the url path
    :param db: Session: Get a database session
    :param current_user: User: Get the user who is currently logged in
    :param : Get the id of the comment to be deleted
    :return: The comment that was deleted
    :doc-author: Trelent
    """
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


@router.get("/get_comment_id/", response_model=CommentModel)
async def get_comment_photo_user_id_route(
    db: Session = Depends(get_db),
    user_id: int = None,
    photo_id: int = None,
    current_user: User = Depends(auth_service.get_current_user_s),
):
    """
    The get_comment_photo_user_id_route function returns a list of comments for the specified photo_id and user_id.
        If user_id is not specified, it will return comments for the current logged in user.

    :param db: Session: Get the database session
    :param user_id: int: Get the comments of a specific user
    :param photo_id: int: Get the photo_id from the url
    :param current_user: User: Get the current user's id
    :param : Get the database connection
    :return: A list of comments from the database
    :doc-author: Trelent
    """
    if not user_id:
        user_id = current_user.id
    if not photo_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user_id cannot be empty"
        )
    return await repository_comments.get_comment_photo_user_id(db, photo_id, user_id)


@router.get("/get_comment_photo_id/{photo_id}", response_model=List[CommentModel])
async def get_comment_photo_id_route(
    photo_id: int,
    db: Session = Depends(get_db),
):
    """
    The get_comment_photo_id_route function returns all comments to a picture (photo_id).

    :param photo_id: int: Get the photo_id from the url
    :param db: Session: Get the database session
    :param : Get the comment by photo id
    :return: A comment object with the photo_id
    :doc-author: Trelent
    """
    comment = repository_comments.get_comment_photo_id(db, photo_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    return comment
