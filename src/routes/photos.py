from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    File,
    Form,
    UploadFile,
    Path,
)
from sqlalchemy.orm import Session

from src.database.db import get_db

# from src.database.models import User
from src.schemas.photos import PhotoResponse, CommentModel
from src.repository import photos as repository_photos

# import src.services.auth as auth

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post(
    "/create/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED
)
async def create_photo(
    file: UploadFile = File(...),
    title: str = Form(None),
    description: str = Form(None),
    tags: List[str] = Form(None),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.create_photo(title, description, tags, file, db)
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo


@router.get("/get", response_model=List[PhotoResponse])
async def show_all_user_photos(db: Session = Depends(get_db)):
    return await repository_photos.get_photos(db)


@router.get("/all", response_model=List[PhotoResponse])
async def show_all_photos(db: Session = Depends(get_db)):
    return await repository_photos.get_photos(db)


@router.get("/by_id/{photo_id}", response_model=PhotoResponse)
async def show_photo_by_id(
    photo_id: int = Path(description="The ID of the photo to get"),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.get_photo(photo_id, db)
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo


@router.get("/comments/all/{photo_id}", response_model=List[CommentModel])
async def show_photo_comments():
    pass


@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(
    photo_id: int = Path(description="The ID of the photo to get"),
    file: UploadFile = File(None),
    title: str = Form(None),
    description: str = Form(None),
    tags: List[str] = Form(None),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.update_photo(
        photo_id, title, description, tags, file, db
    )
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo


@router.delete("/{photo_id}", response_model=PhotoResponse)
async def remove_photo(
    photo_id: int = Path(description="The ID of the photo to get"),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.remove_photo(photo_id, db)
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo
