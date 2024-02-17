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
async def create_tag():
    pass


@router.get("/all/", response_model=List[TagResponse])
async def read_all_tags():
    pass


@router.get("/by_id/{tag_id}", response_model=TagResponse)
async def read_tag_by_id():
    pass


@router.put("/change_tag/{tag_id}", response_model=TagResponse)
async def update_tag():
    pass


@router.delete("/del/{tag_id}", response_model=TagResponse)
async def remove_tag():
    pass




