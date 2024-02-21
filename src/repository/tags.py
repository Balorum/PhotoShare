from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Tag, User
from src.schemas.photos import TagBase, TagModel


async def get_my_tags(tag_id: int, user: User, db: Session) -> List[Tag]:
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == 1)).first()

async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    Creates a new tag for our API.
    
    :param body: Get the title of the tag from the request body
    :type body: TagModel
    :param user: Get the user id of the current user
    :type user: User
    :param db: Access the database
    :type db: Session
    :return: Tag object
    :rtype: Tag
    """
    val_title = body.title
    val_title = val_title.lower()
    tag = db.query(Tag).filter(Tag.title == val_title.lower()).first()
    if tag == None:
        tag = Tag(
            title=val_title,
            user_id = 1,
        )
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


async def get_all_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    Returns all tags of our API.
    
    :param skip: The number of tags to skip.
    :type skip: int
    :param limit: The maximum number of tags to return.
    :type limit: int
    :param user: The user to retrieve tags for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of tags.
    :rtype: List[Tag]
    """
    return db.query(Tag).offset(skip).limit(limit).all()


async def update_tag(tag_id: int, body: TagBase, user: User, db: Session) -> Tag | None:
    """
    Update tag.
    
    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param body: Get the new fields of the tag from the request body.
    :type body: TagBase
    :param user: The user to update tag for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Tag object.
    :rtype: Tag
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.title = body.title
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Tag | None:
    """
    Delete tag.
    
    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param user: The user to delete tag for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Tag object.
    :rtype: Tag
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag



