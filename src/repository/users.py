from libgravatar import Gravatar
from datetime import datetime
from typing import List

import cloudinary
import cloudinary.uploader
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.conf.config import init_cloudinary
from src.database.models import User, Role, Comment, Photo
from src.schemas.users import UserModel, RequestEmail, UserProfileModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email.

    :param email: str: Specify the type of parameter that will be passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    return db.query(User).filter(User.email == email).first()


async def get_me(user: User, db: Session):
    """
    The get_me function returns the user object of the currently logged in user.

    :param user: User: Pass the user object to the function
    :param db: Session: Access the database
    :return: A user object
    """

    return db.query(User).filter(User.id == user.id).first()


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


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of parameter that is being passed into the function
    :param db: Session: Pass the database session to the function
    :return: The user object
    """

    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user(body: RequestEmail, owner_id: int, db: Session):
    user = db.query(User).filter_by(id=owner_id).first()
    if user:
        user.email = body.email
        db.commit()
    return user


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


async def get_users(skip: int, limit: int, db: Session) -> List[User]:
    """
    The get_users function returns a list of users from the database.

    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of users
    """

    return db.query(User).offset(skip).limit(limit).all()    


async def get_user_profile(username: str, db: Session) -> User:
    """
    The get_user_profile function returns a UserProfileModel object containing the user's username, email, avatar, created_at date and time (in UTC), is_active status (True or False), photo count and comment count.

    :param username: str: Get the username of the user who is trying to access their profile
    :param db: Session: Pass in the database session to the function
    :return: A user object
    """

    user = db.query(User).filter(User.username == username).first()
    if user:
        photo_count = db.query(Photo).filter(Photo.user_id == user.id).count()

        comment_count = (
            db.query(Comment).filter(Comment.user_id == user.id).count()
        )
        user_profile = UserProfileModel(
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            created_at=user.created_at,
            is_active=user.is_active,
            photo_count=photo_count,
            comment_count=comment_count,
        )
        return user_profile
    
async def change_user_role(email: str, role: str, db: Session) -> None:
    """
    The change_user_role function takes an email and a role, then finds the user with that email in the database.
    It then sets that user's role to be equal to the given role.

    :param email: str: Get the user by email
    :param role: Role: Specify the role of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """

    user = await get_user_by_email(email, db)
    user.role = role
    db.commit() 


async def ban_user(email: str, db: Session) -> None:
    """
    The ban_user function takes an email address and a database connection,
    and sets the user.is_active to False.
        
    :param email: str: Specify the email of the user to ban
    :param db: Session: Pass the database session to the function
    :return: None
    """
    
    user = await get_user_by_email(email, db)
    user.is_active = False
    db.commit()


async def remove_from_ban(email: str, db: Session) -> None:
    """
    The remove_from_ban function removes a user from the ban list.

    :param email: str: Get the user by email
    :param db: Session: database session
    :return: None
    """

    user = await get_user_by_email(email, db)
    user.is_active = True
    db.commit()