from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from typing import List

# from src.database.models import User
# from src.database.db import get_db
from src.schemas.photos import CommentBase, CommentUpdate, CommentModel
# from src.repository import comments as repository_comments
# from src.services.auth import auth_service
# from src.database.models import User

router = APIRouter(prefix='/comments', tags=["comments"])


@router.post("/create/{photo_id}", response_model=CommentModel)
async def create_comment():
    pass


@router.put("/edit/{comment_id}", response_model=CommentUpdate)
async def edit_comment():
    pass


@router.delete("/delete/{comment_id}", response_model=CommentModel)
async def delete_comment():
    pass



