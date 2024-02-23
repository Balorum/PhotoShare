from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Request, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.photos import RatingModel, PhotoResponse
from src.repository import ratings as repository_ratings
from src.services.auth import auth_service

from src.database.models import User, UserRoleEnum
from src.conf import messages as message

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post(
    "/photos/{photo_id}/{rate}",
    response_model=RatingModel,
)
async def create_rate(
    photo_id: int,
    rate: int = Path(description="From one to five stars of rating.", ge=1, le=5),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

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
    new_rate: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    edited_rate = await repository_ratings.edit_rate(
        rate_id, new_rate, db, current_user
    )
    if edited_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
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

    comments = await repository_ratings.show_my_ratings(db, current_user)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such rating"
        )
    return comments


@router.get(
    "/user_post/{user_id}/{post_id}",
    response_model=RatingModel,
)
async def user_rate_post(
    user_id: int,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

    rate = await repository_ratings.user_rate_post(user_id, post_id, db, current_user)
    if rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return rate
