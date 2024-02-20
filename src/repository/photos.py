from typing import List, Annotated

from datetime import datetime

import cloudinary
import cloudinary.uploader

from fastapi import Request, UploadFile, Query
from sqlalchemy.orm import Session

from src.database.models import Photo, Tag, User, Comment
from src.conf.config import settings, cloud_init


async def get_photos(db: Session) -> List[Photo]:
    return db.query(Photo).all()


async def get_photo(photo_id: int, db: Session) -> Photo:
    return db.query(Photo).filter(Photo.id == photo_id).first()


async def create_photo(title: Annotated[str, Query(max_length=50)],
                       description: Annotated[str, Query(max_length=150)],
                       tags: List[str],
                       file: UploadFile,
                       db: Session) -> Photo:
    cloud_init()
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShareApp/user',
                                   overwrite=True)  # Коли буде функціонал, вказати конкретного юзера
    src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/user') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    if tags:
        tags = create_or_get_tag(tags[0].split(","), 1, db)
    new_photo = Photo(image_url=src_url, title=title, created_at=datetime.now(), tags=tags, description=description)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


async def remove_photo(photo_id: int, db: Session) -> Photo | None:
    new_photo = await get_photo(photo_id, db)
    if new_photo:
        db.delete(new_photo)
        db.commit()
    return new_photo


async def update_photo(photo_id: int,
                       title: Annotated[str, Query(max_length=50)],
                       description: Annotated[str, Query(max_length=150)],
                       tags: List[str],
                       file: UploadFile,
                       db: Session) -> Photo | None:
    new_photo = await get_photo(photo_id, db)
    if new_photo:
        new_photo.title = title if title else new_photo.title
        new_photo.description = description if description else new_photo.description
        new_photo.tags = create_or_get_tag(tags[0].split(","), 1, db) if tags else new_photo.description
        if file:
            cloud_init()
            r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShareApp/user',
                                           overwrite=True)  # Коли буде функціонал, вказати конкретного юзера
            src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/user') \
                .build_url(width=250, height=250, crop='fill', version=r.get('version'))
            new_photo.image_url = src_url
        new_photo.updated_at = datetime.now()
        db.commit()

    return new_photo

def create_or_get_tag(titles: list[str], user: int, db: Session):
    tags = []
    for title in titles:
        tag = db.query(Tag).filter(Tag.title == title.lower()).first()
        if not tag:
            tag = Tag(
            title=title.lower(),
            user_id = user,
            )
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    return tags
