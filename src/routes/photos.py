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
from src.database.models import User, Role
from src.database.models import Tag
from src.schemas.photos import PhotoResponse, CommentModel
from src.repository import photos as repository_photos
from src.services.auth import auth_service
from src.services.roles import RoleChecker

router = APIRouter(prefix="/photos", tags=["photos"])

access_get = RoleChecker([Role.admin, Role.moderator, Role.user])
access_update = RoleChecker([Role.admin, Role.moderator, Role.user])
access_admin = RoleChecker([Role.admin])


@router.post(
    "/create/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED
)
async def create_photo(
    file: UploadFile = File(...),
    title: str = Form(None),
    current_user: User = Depends(auth_service.get_current_user),
    description: str = Form(None),
    tags: List[str] = Form(None),
    db: Session = Depends(get_db),
):
    if len(tags[0].split(",")) >= 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There cannot be more than five tags",
        )
    new_photo = await repository_photos.create_photo(
        title, description, tags, current_user, file, db
    )
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo


@router.get("/get_by_user/{user_id}", response_model=List[PhotoResponse])
async def show_all_user_photos(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    posts = await repository_photos.get_user_photos(skip, limit, current_user, db)
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found"
        )
    return posts


@router.get("/all", response_model=List[PhotoResponse])
async def show_all_photos(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await repository_photos.get_photos(skip, limit, db)


@router.get("/by_id/{photo_id}", response_model=PhotoResponse)
async def show_photo_by_id(
    photo_id: int = Path(description="The ID of the photo to get"),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.get_photo(photo_id, current_user, db)
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
    current_user: User = Depends(auth_service.get_current_user),
    tags: List[str] = Form(None),
    db: Session = Depends(get_db),
):
    if len(tags[0].split(",")) >= 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There cannot be more than five tags",
        )
    new_photo = await repository_photos.update_photo(
        photo_id, title, description, tags, current_user, file, db
    )
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo


@router.delete("/{photo_id}", response_model=PhotoResponse)
async def remove_photo(
    photo_id: int = Path(description="The ID of the photo to get"),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    new_photo = await repository_photos.remove_photo(photo_id, current_user, db)
    if new_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_photo
