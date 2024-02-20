from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.database.models import User
from src.schemas.photos import PhotoResponse, RequestRole
from src.schemas.users import UserModel, UserResponse
from src.services.auth import auth_service

from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
from src.repository import users as repositories_users


router = APIRouter(prefix="/users", tags=["users"])

"""
@router.get("/me/", response_model=UserResponse)
async def read_my_profile():
    pass


@router.put("/edit_prof/", response_model=UserResponse)
async def edit_profile():
    pass
"""


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    #auth_service.cache.set(user.email, pickle.dumps(user))
    #auth_service.cache.expire(user.email, 300)
    return user
