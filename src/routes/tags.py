from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.photos import TagBase, TagResponse
from src.repository import tags as repository_tags
from src.database.models import User
from src.services.auth import auth_service


router = APIRouter(prefix='/tags', tags=["tags"])

@router.post("/create/", response_model=TagResponse)
async def create_tag(body: TagBase, db: Session = Depends(get_db),
                     current_user: str = "Some_User"):
    return await repository_tags.create_tag(body, current_user, db)


@router.get("/all/", response_model=List[TagResponse])
async def read_all_tags(skip: int = 0, limit: int = 100, current_user: str = "Some_User", db: Session = Depends(get_db)):
    return await repository_tags.get_all_tags(skip, limit, current_user, db)


@router.get("/by_id/{tag_id}", response_model=TagResponse)
async def read_tag_by_id(tag_id: int, db: Session = Depends(get_db),
            current_user: str = "Some_User"):
    tag = await repository_tags.get_my_tags(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag


@router.put("/change_tag/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, body: TagBase, db: Session = Depends(get_db),
            current_user: str = "Some_User"):
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag


@router.delete("/del/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db),
            current_user: str = "Some_User"):
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag




