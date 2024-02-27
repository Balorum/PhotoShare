from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from starlette import status

from src.database.models import Rating, User, Photo


async def create_rate(photo_id: int, rate: int, db: Session, user: User) -> Rating:

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

    all_ratings = db.query(Rating).all()
    return all_ratings


async def show_my_ratings(db: Session, user: User) -> list[Type[Rating]]:

    all_ratings = db.query(Rating).filter(Rating.user_id == user.id).all()
    return all_ratings


async def user_rate_post(
    user_id: int, photo_id: int, db: Session, user: User
) -> Type[Rating] | None:

    user_p_rate = (
        db.query(Rating)
        .filter(and_(Rating.photo_id == photo_id, Rating.user_id == user_id))
        .first()
    )
    return user_p_rate
