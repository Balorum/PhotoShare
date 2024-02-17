from typing import List
from datetime import datetime

import cloudinary
import cloudinary.uploader

from fastapi import Request, UploadFile
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from src.conf.config import init_cloudinary
from src.database.models import Photo, Tag, User, Comment
from src.schemas.photos import PhotoUpdate


async def get_photos() -> List[Photo]:
    pass


async def get_photo() -> Photo:
    pass


async def create_photo() -> Photo:
    pass


async def remove_photo() -> Photo | None:
    pass


async def update_photo() -> Photo | None:
    pass



