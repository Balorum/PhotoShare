from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.schemas.photos import PhotoModel, PhotoUpdate, PhotoStatusUpdate, PhotoResponse, CommentModel
from src.repository import photos as repository_photos
import src.services.auth as auth

router = APIRouter(prefix='/photos', tags=["photos"])

@router.post("/create/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo():
    pass

@router.get("/get", response_model=List[PhotoResponse])
async def show_all_user_photos():
    pass


@router.get("/all", response_model=List[PhotoResponse])
async def show_all_photos():
    pass


@router.get("/by_id/{photo_id}", response_model=PhotoResponse)
async def show_photo_by_id():
    pass

@router.get("/comments/all/{photo_id}", response_model=List[CommentModel])
async def show_ppoto_comments():
    pass

@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo():
    pass

@router.delete("/{photo_id}", response_model=PhotoResponse)
async def remove_photo():
    pass








