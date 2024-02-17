from datetime import datetime
from typing import List

import cloudinary
import cloudinary.uploader
from sqlalchemy import  func
from sqlalchemy.orm import Session

from src.conf.config import init_cloudinary
from src.database.models import User, Comment, Photo
from src.schemas.users import UserModel


async def create_user() -> User:
    pass


async def update_token() -> None:
    pass


async def update_avatar() -> User:
    pass
