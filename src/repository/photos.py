from typing import List, Annotated

from datetime import datetime

import cloudinary
import cloudinary.uploader

from fastapi import Request, UploadFile, Query
from sqlalchemy.orm import Session

from src.database.models import Photo, Tag, User, Comment, Role
from src.conf.config import settings, cloud_init


async def get_photos(skip, limit, db: Session) -> List[Photo]:
    """
    Get list of photos with the specified number
    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit:The maximum number of contact to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: a list of photos
    :rtype: List[Photo]
    """
    return db.query(Photo).offset(skip).limit(limit).all()


async def get_user_photos(skip, limit, current_user, db) -> List[Photo]:
    """
    Get list of photo with the specified number of them for a specific user.
    :param skip: The number of photos to skip.
    :type skip: int
    :param limit:The maximum number of photos to return.
    :type limit: int
    :param current_user: The user to retrieve photos for.
    :type current_user: User
    :param db: The database session
    :type db: Session
    :return: a list of photos
    :rtype: List[Photo]
    """
    return (
        db.query(Photo)
        .filter(Photo.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_photo(photo_id: int, current_user: User, db: Session) -> Photo:
    """
    Get a photo of the specified id
    :param photo_id: id of the photo
    :type photo_id: int
    :param current_user: The user to retrieve photos for.
    :type current_user: User
    :param db: The database session
    :type db: Session
    :return: Photo of the specified id
    :rtype: Photo
    """
    return db.query(Photo).filter(Photo.id == photo_id).first()


async def get_photo_by_id(photo_id: int, current_user: User, db: Session) -> Photo:
    """
    Get a photo with the specified id for a specific user and filter by user_role
    :param photo_id: id of the photo
    :type photo_id: int
    :param current_user: The user to retrieve photos for.
    :type current_user: User
    :param db: The database session
    :type db: Session
    :return: photo filtered by role
    :rtype: Photo
    """
    if current_user.role == "admin":
        return db.query(Photo).filter(Photo.id == photo_id).first()
    else:
        return (
            db.query(Photo)
            .filter(Photo.user_id == current_user.id)
            .filter(Photo.id == photo_id)
            .first()
        )


async def create_photo(
    title: Annotated[str, Query(max_length=50)],
    description: Annotated[str, Query(max_length=150)],
    tags: List[str],
    current_user: User,
    file: UploadFile,
    db: Session,
) -> Photo:
    """
    Create a new photo for a specific user
    :param title: title of the photo
    :type title: str
    :param description: description of the photo
    :type description: str
    :param tags: tags of the photo
    :type tags: List[Tag]
    :param current_user: The user to create the photo for
    :type current_user: User
    :param file: image
    :type file: UploadFile
    :param db: The database session
    :type db: Session
    :return: photo created
    :rtype: Photo
    """
    cloud_init()

    r = cloudinary.uploader.upload(
        file.file, public_id=f"PhotoShareApp/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(
        f"PhotoShareApp/{current_user.username}"
    ).build_url(width=250, height=250, crop="fill", version=r.get("version"))
    if tags != [""]:
        tags = create_or_get_tag(tags[0].split(","), current_user.id, db)
    else:
        tags = []
    new_photo = Photo(
        image_url=src_url,
        title=title,
        user_id=current_user.id,
        created_at=datetime.now(),
        tags=tags,
        description=description,
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


async def remove_photo(photo_id: int, current_user: User, db: Session) -> Photo | None:
    """
    Remove a photo
    :param photo_id: id photo to remove
    :param current_user: The user to retrieve photos for.
    :type current_user: User
    :param db: The database session
    :type db: Session
    :return: photo or None
    :rtype: Photo | None
    """
    new_photo = await get_photo_by_id(photo_id, current_user, db)
    if new_photo:
        db.delete(new_photo)
        db.commit()
    return new_photo


async def update_photo(
    photo_id: int,
    title: Annotated[str, Query(max_length=50)],
    description: Annotated[str, Query(max_length=150)],
    tags: List[str],
    current_user: User,
    file: UploadFile,
    db: Session,
) -> Photo | None:
    """
    Update a photo for a specific user by specific id
    :param photo_id: id photo to update
    :type photo_id: int
    :param title: title of the photo
    :type title: str
    :param description: description of the photo
    :rtype description: str

    :param tags: tags of the photo
    :type tags: List[Tag]
    :param current_user: user who updated the photo
    :type current_user: User
    :param file: file of the photo
    :type: UploadFile
    :param db: The database session
    :type db: Session
    :return: the updated photo
    :rtype: Photo
    """
    new_photo = await get_photo_by_id(photo_id, current_user, db)
    if new_photo:
        new_photo.title = title if title else new_photo.title
        new_photo.description = description if description else new_photo.description
        new_photo.tags = (
            create_or_get_tag(tags[0].split(","), current_user.id, db)
            if (tags != [""] and tags != None)
            else []
        )

        if file:
            cloud_init()
            r = cloudinary.uploader.upload(
                file.file,
                public_id=f"PhotoShareApp/{current_user.username}",
                overwrite=True,
            )
            src_url = cloudinary.CloudinaryImage(
                f"PhotoShareApp/{current_user.username}"
            ).build_url(width=250, height=250, crop="fill", version=r.get("version"))
            new_photo.image_url = src_url
        new_photo.updated_at = datetime.now()
        db.commit()

    return new_photo


def create_or_get_tag(titles: list[str], user_id: int, db: Session):
    """
    Create or get tag
    :param titles: titles of the tags
    :type tags: list[str]
    :param user_id: the id of the user
    :type user_id: int
    :param db: The database session
    :type db: Session
    :return: list of tags
    :rtype: List[Tag]
    """
    tags = []
    for title in titles:
        tag = db.query(Tag).filter(Tag.title == title.lower()).first()
        if not tag:
            tag = Tag(
                title=title.lower(),
                user_id=user_id,
            )
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    return tags
