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
    Query,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.transform import TransformModel, TransformResponse
from src.repository import transforms as repository_transforms

router = APIRouter(prefix="/transforms", tags=["transforms"])


@router.put("{photo_id}")
async def edit_photo(
    transform: TransformModel,
    photo_id: int = Path(description="The ID of the photo to get", gt=0),
    db: Session = Depends(get_db),
):
    new_url = await repository_transforms.get_transform_url(photo_id, transform, db)
    if new_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_url
