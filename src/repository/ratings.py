from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from starlette import status

from src.database.models import Rating, User, Photo


async def create_rate(photo_id: int, rate: int, db: Session, user: User) -> Rating:
    """
    The create_rate function creates a new rate for the photo with the given id.
        The user who is creating this rate must be logged in and cannot create a rating for their own photo.
        If they have already created a rating, they will receive an error message.

    :param photo_id: int: Get the photo id from the request body
    :param rate: int: Get the rate value from the request body
    :param db: Session: Access the database
    :param user: User: Check if the user is trying to rate his own photo
    :return: The new_rate object, which is a rating instance
    """
    is_self_post = (
        db.query(Photo)
        .filter(and_(Photo.id == photo_id, Photo.user_id == user.id))
        .first()
    )
    already_voted = (
        db.query(Rating)
        .filter(and_(Rating.photo_id == photo_id, Rating.user_id == user.id))
        .first()
    )
    photo_exists = db.query(Photo).filter(Photo.id == photo_id).first()
    if is_self_post:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED, detail="You can`t rate your own photo"
        )
    elif already_voted:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="You can`t rate the same photo twice",
        )
    elif photo_exists:
        new_rate = Rating(photo_id=photo_id, rate=rate, user_id=user.id)
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return new_rate


async def edit_rate(
    rate_id: int, new_rate: int, db: Session, user: User
) -> Type[Rating] | None:
    """
    The edit_rate function allows a user to edit their own rating.
        Args:
            rate_id (int): The id of the rating that is being edited.
            new_rate (int): The new value for the rating.  Must be between 1 and 5 inclusive.
            db (Session): A database session object used to query the database for ratings and commit changes made by this function back into the database.
            user (User): An object representing a logged in user, which is used to verify that they are editing their own rate, not someone else's.

    :param rate_id: int: Find the rate in the database
    :param new_rate: int: Get the new rate value from the request body
    :param db: Session: Access the database
    :param user: User: Check if the user who is trying to edit the rate is actually the owner of that rate
    :return: None if the rate does not exist, or returns a rating object
    """
    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if rate:
        if rate.user_id == user.id:
            rate.rate = new_rate
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="You can`t edit someone else's rate",
            )
    return rate


async def delete_rate(rate_id: int, db: Session, user: User) -> Type[Rating]:
    """
    The delete_rate function deletes a rate from the database.
        Args:
            rate_id (int): The id of the rate to delete.
            db (Session, optional): SQLAlchemy Session. Defaults to None.
            user (User, optional): User object with role information for authorization purposes.. Defaults to None.&lt;/code&gt;

    :param rate_id: int: Identify the rate to be deleted
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is an admin or moderator
    :return: The deleted rate&lt;/code&gt;
    """
    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if user.role in ["admin", "moderator"] or rate.user_id == user.id:
        if rate:
            db.delete(rate)
            db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="You can`t delete someone else's rate",
        )
    return rate


async def show_ratings(db: Session, user: User) -> list[Type[Rating]]:
    """
    The show_ratings function returns a list of all ratings in the database.


    :param db: Session: Access the database
    :param user: User: Get the user's id
    :return: A list of rating objects
    """
    all_ratings = db.query(Rating).all()
    return all_ratings


async def show_my_ratings(db: Session, user: User) -> list[Type[Rating]]:
    """
    The show_my_ratings function returns a list of all the ratings that a user has made.


    :param db: Session: Pass the database session to the function
    :param user: User: Get the user id from the database
    :return: A list of rating objects
    """
    all_ratings = db.query(Rating).filter(Rating.user_id == user.id).all()
    return all_ratings


async def user_rate_post(
    user_id: int, photo_id: int, db: Session, user: User
) -> Type[Rating] | None:
    """
    The user_rate_post function is used to check if a user has already rated a photo.
        If the user has not yet rated the photo, then they will be able to rate it.
        If they have already rated it, then their rating will be updated.

    :param user_id: int: Get the user_id from the database
    :param photo_id: int: Get the photo id from the database
    :param db: Session: Access the database
    :param user: User: Get the user_id of the current logged in user
    :return: A rating object
    """
    user_p_rate = (
        db.query(Rating)
        .filter(and_(Rating.photo_id == photo_id, Rating.user_id == user_id))
        .first()
    )
    return user_p_rate
