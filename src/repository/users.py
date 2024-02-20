from libgravatar import Gravatar
from datetime import datetime
from typing import List

import cloudinary
import cloudinary.uploader
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.conf.config import cloud_init
from src.database.models import User, Role, Comment, Photo

from src.schemas.users import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email.

    :param email: str: Specify the type of parameter that will be passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :return: A user object
    """

    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    new_user.role = "user"
    result = db.query(User).all()
    userscount = len(result)
    if not userscount:
        new_user.role = "admin"
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Update the refresh_token field in the user table
    :param db: Session: Commit the changes to the database
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def update_avatar() -> User:
    pass


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.

    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
