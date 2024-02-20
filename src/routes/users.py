from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

# from src.database.db import get_db
# from src.repository import users as repository_users
# from src.database.models import User
# from src.schemas.photos import PhotoResponse, RequestRole
from src.schemas.users import UserModel, UserResponse

# from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_my_profile():
    pass


@router.put("/edit_prof/", response_model=UserResponse)
async def edit_profile():
    pass
