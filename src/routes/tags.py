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
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new tag for our API.
    
    :param body: Get the title of the tag from the request body
    :type body: TagModel
    :param db: Access the database
    :type db: Session
    :param user: Get the user id of the current user
    :type user: User
    :return: Tag object
    :rtype: Tag
    """
    return await repository_tags.create_tag(body, current_user, db)


@router.get("/all/", response_model=List[TagResponse])
async def read_all_tags(skip: int = 0, limit: int = 100, 
                        current_user: User = Depends(auth_service.get_current_user), 
                        db: Session = Depends(get_db)):
    """
    Returns all tags of our API.
    
    :param skip: The number of tags to skip.
    :type skip: int
    :param limit: The maximum number of tags to return.
    :type limit: int
    :param user: The user to retrieve tags for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of tags.
    :rtype: List[Tag]
    """
    return await repository_tags.get_all_tags(skip, limit, current_user, db)


@router.get("/by_id/{tag_id}", response_model=TagResponse)
async def read_tag_by_id(tag_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(auth_service.get_current_user)):
    """
    Search tag by its id.
    
    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :param user: The user to update tag for.
    :type user: User
    :return: Tag object.
    :rtype: Tag
    """
    tag = await repository_tags.get_my_tags(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag


@router.put("/change_tag/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, body: TagBase, db: Session = Depends(get_db),
            current_user: User = Depends(auth_service.get_current_user)):
    """
    Update tag.
    
    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param body: Get the new fields of the tag from the request body.
    :type body: TagBase
    :param db: The database session.
    :type db: Session
    :param user: The user to update tag for.
    :type user: User
    :return: Tag object.
    :rtype: Tag
    """
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag


@router.delete("/del/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete tag.
    
    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :param user: The user to delete tag for.
    :type user: User
    :return: Tag object.
    :rtype: Tag
    """
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404_TAG_NOT_FOUND")
    return tag
