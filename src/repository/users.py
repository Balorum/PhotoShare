# repository/users.py
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database.models import User
from src.schemas.users import UserModel

async def create_user(db: Session, body: UserModel) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return await db.query(User).filter(User.email == email).first()

async def update_token(db: Session, user: User, token: str) -> None:
    user.refresh_token = token
    await db.commit()

async def update_avatar(db: Session, email: str, url: str) -> User:
    user = await get_user_by_email(db, email)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
