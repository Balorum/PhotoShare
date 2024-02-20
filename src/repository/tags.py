from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Tag, User
from src.schemas.photos import TagBase, TagModel


async def create_user(db: Session):
    user = User(
        username="username",
        email="email",
        password="password",
        avatar="avatar",
        role="admin",
        confirmed=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_my_tags(tag_id: int, user: str, db: Session) -> List[Tag]:
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == 1)).first()


async def create_tag(body: TagModel, user: str, db: Session) -> Tag:
    # user = await create_user(db)
    val_title = body.title
    val_title = val_title.lower()
    tag = db.query(Tag).filter(Tag.title == val_title.lower()).first()
    if tag == None:
        tag = Tag(
            title=val_title,
            user_id=1,
        )
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


async def get_all_tags(skip: int, limit: int, user: str, db: Session) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


async def update_tag(tag_id: int, body: TagBase, user: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.title = body.title
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
