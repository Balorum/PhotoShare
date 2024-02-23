from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from starlette import status

from src.database.models import Rating, User, Post, UserRoleEnum
from src.conf import messages as message


async def create_rate(post_id: int, rate: int, db: Session, user: User) -> Rating:

    is_self_post = (
        db.query(Post).filter(and_(Post.id == post_id, Post.user_id == user.id)).first()
    )
    already_voted = (
        db.query(Rating)
        .filter(and_(Rating.post_id == post_id, Rating.user_id == user.id))
        .first()
    )
    post_exists = db.query(Post).filter(Post.id == post_id).first()
    if is_self_post:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=message.OWN_POST)
    elif already_voted:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED, detail=message.VOTE_TWICE
        )
    elif post_exists:
        new_rate = Rating(post_id=post_id, rate=rate, user_id=user.id)
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return new_rate


async def edit_rate(
    rate_id: int, new_rate: int, db: Session, user: User
) -> Type[Rating] | None:

    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if user.role in [UserRoleEnum.admin, UserRoleEnum.moder] or rate.user_id == user.id:
        if rate:
            rate.rate = new_rate
            db.commit()
    return rate


async def delete_rate(rate_id: int, db: Session, user: User) -> Type[Rating]:

    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if rate:
        db.delete(rate)
        db.commit()
    return rate


async def show_ratings(db: Session, user: User) -> list[Type[Rating]]:

    all_ratings = db.query(Rating).all()
    return all_ratings


async def show_my_ratings(db: Session, user: User) -> list[Type[Rating]]:

    all_ratings = db.query(Rating).filter(Rating.user_id == user.id).all()
    return all_ratings


async def user_rate_post(
    user_id: int, post_id: int, db: Session, user: User
) -> Type[Rating] | None:

    user_p_rate = (
        db.query(Rating)
        .filter(and_(Rating.post_id == post_id, Rating.user_id == user_id))
        .first()
    )
    return user_p_rate