from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Request, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.photos import RatingModel, PhotoResponse
from src.repository import ratings as repository_ratings
from src.services.auth import auth_service

from src.database.models import User


router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post(
    "/create/{photo_id}/{rate}",
    response_model=RatingModel,
)
async def create_rate(
    photo_id: int,
    rate: int = Path(description="From one to five stars of rating.", ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_rate function creates a new rate for the photo with the given ID.
        The user who created this rate is determined by the JWT token in the Authorization header.
        If there is no such photo, it returns 404 Not Found.

    :param photo_id: int: Get the photo id from the url
    :param rate: int: Get the rating from the user
    :param ge: Check if the rate is greater than or equal to 1
    :param le: Set the maximum value of the rating
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :param : Get the photo_id from the url and to create a new rate
    :return: A dictionary with the photo_id, rate and user_id
    """
    new_rate = await repository_ratings.create_rate(photo_id, rate, db, current_user)
    if new_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no photos ID"
        )
    return new_rate


@router.put(
    "/edit/{rate_id}/{new_rate}",
    response_model=RatingModel,
)
async def edit_rate(
    rate_id: int,
    new_rate: int = Path(description="From one to five stars of rating.", ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The edit_rate function allows a user to edit their rating of a movie.
        The function takes in the rate_id, new_rate, db and current_user as parameters.
        It then calls the edit_rate function from repository/ratings.py which edits the rate in the database and returns it.

    :param rate_id: int: Identify the rate to be edited
    :param new_rate: int: Set the new rate value
    :param ge: Specify the minimum value of a field
    :param le: Limit the value of the new_rate parameter to 5
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :param : Get the id of the rate to be edited
    :return: A dict
    """
    edited_rate = await repository_ratings.edit_rate(
        rate_id, new_rate, db, current_user
    )
    if edited_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found"
        )
    return edited_rate


@router.delete(
    "/delete/{rate_id}",
    response_model=RatingModel,
)
async def delete_rate(
    rate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_rate function deletes a rate from the database.
        It takes in an id of the rate to be deleted and returns a JSON object with information about the deleted rate.

    :param rate_id: int: Identify the rate that is to be deleted
    :param db: Session: Pass the database session to the repository function
    :param current_user: User: Get the user id from the token
    :param : Get the rate_id from the url
    :return: A dictionary with the id of the deleted rate
    """
    deleted_rate = await repository_ratings.delete_rate(rate_id, db, current_user)
    if deleted_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such rating"
        )
    return deleted_rate


@router.get(
    "/all",
    response_model=List[RatingModel],
)
async def all_rates(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The all_rates function returns all ratings for a given user.


    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :param : Pass the database connection to the function
    :return: A list of all ratings in the database
    """
    comments = await repository_ratings.show_ratings(db, current_user)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such rating"
        )
    return comments


@router.get(
    "/all_my",
    response_model=List[RatingModel],
)
async def all_my_rates(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The all_my_rates function returns all the ratings that a user has made.


    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current logged in user
    :param : Get the current user from the database
    :return: A list of comments
    """
    comments = await repository_ratings.show_my_ratings(db, current_user)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such rating"
        )
    return comments


@router.get(
    "/user_photo/{user_id}/{photo_id}",
    response_model=RatingModel,
)
async def user_rate_post(
    user_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The user_rate_post function allows a user to rate another user's post.
        The function takes in the following parameters:
            -user_id: the id of the user whose post is being rated.
            -photo_id: the id of the photo that is being rated.

    :param user_id: int: Get the user_id of the user who is rating a post
    :param photo_id: int: Get the photo id from the url
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user that is currently logged in
    :param : Get the user_id of the user who is rating
    :return: A dict with the following keys:
    """
    rate = await repository_ratings.user_rate_post(user_id, photo_id, db, current_user)
    if rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return rate
