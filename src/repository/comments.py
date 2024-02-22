from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment
from src.schemas.comments import CommentBase, CommentModel, CommentUpdate


async def create_comment(
    db: Session, comment_data: CommentModel, photo_id: int, user_id: int
):
    """
    The create_comment function creates a new comment for an image.
        Args:
            db (Session): The database session to use for creating the comment.
            comment_data (CommentModel): The data of the new Comment object to create.
            photo_id (int): The id of the Photo that this Comment is associated with.
            user_id (int): The id of the User that created this Comment.

    :param db: Session: Pass the database session to the function
    :param comment_data: CommentModel: Pass the data of a comment to the function
    :param photo_id: int: Identify the photo that the comment is being made on
    :param user_id: int: Identify the user who created the comment
    :return: The comment object that was created
    :doc-author: Trelent
    """
    comment = Comment(
        text=comment_data.text,
        user_id=user_id,
        photo_id=photo_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def get_comment(db: Session, comment_id: int):
    """
    The get_comment function returns a comment object from the database.

    :param db: Session: Pass in the database session
    :param comment_id: int: Filter the comment by id
    :return: A comment object
    :doc-author: Trelent
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


async def get_comment_photo_user_id(db: Session, photo_id: int, user_id: int):
    """
    The get_comment_photo_user_id function returns the comment (with photo_id) of the user with user_id.
        Args:
            db (Session): The database session to use for querying.
            photo_id (int): The id of the photo to query comments from.
            user_id (int): The id of the user who made a comment on this photo.

    :param db: Session: Create a database session
    :param photo_id: int: Filter the comments by photo_id
    :param user_id: int: Filter the comments by user_id
    :return: A comment object
    :doc-author: Trelent
    """
    return (
        db.query(Comment)
        .filter(Comment.photo_id == photo_id, Comment.user_id == user_id)
        .first()
    )


async def get_comment_photo_id(db: Session, photo_id: int):
    """
    The get_comment_photo_id function takes in a photo_id and returns the comment associated with that photo.
        Args:
            db (Session): The database session to use for querying.
            photo_id (int): The id of the Photo object to query for.
        Returns:
            Comment: A Comment object containing all information about a given comment.

    :param db: Session: Pass the database session into the function
    :param photo_id: int: Filter the comment by photo_id
    :return: A comment object
    :doc-author: Trelent
    """
    return db.query(Comment).filter(Comment.photo_id == photo_id).first()


async def edit_comment(db: Session, comment_id: int, new_text: str):
    """
    The edit_comment function allows a user to edit an existing comment.
        Args:
            db (Session): The database session object.
            comment_id (int): The id of the comment to be edited.
            new_text (str): The new text for the edited comment.

    :param db: Session: Pass the database session to the function
    :param comment_id: int: Get the comment from the database
    :param new_text: str: Pass the new text to be updated in the comment
    :return: The comment object
    :doc-author: Trelent
    """
    comment = await get_comment(db, comment_id)
    if comment:
        comment.text = new_text
        comment.updated_at = datetime.now()
        comment.update_status = True
        db.commit()
        db.refresh(comment)
    return comment


async def delete_comment(db: Session, comment_id: int):
    """
    The delete_comment function deletes a comment from the database.

    :param db: Session: Connect to the database
    :param comment_id: int: Specify which comment to delete
    :return: The deleted comment
    :doc-author: Trelent
    """
    comment = await get_comment(db, comment_id)
    if comment:
        db.delete(comment)
        db.commit()
    return comment
