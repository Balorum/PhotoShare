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
    Response,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.services.auth import auth_service
from src.schemas.transform import TransformModel, TransformResponse
from src.repository import transforms as repository_transforms
from src.services.roles import RoleChecker

router = APIRouter(prefix="/transforms", tags=["transforms"])
access_get = RoleChecker([Role.admin, Role.moderator, Role.user])
access_update = RoleChecker([Role.admin, Role.moderator, Role.user])
access_admin = RoleChecker([Role.admin])


@router.post("{photo_id}", dependencies=[Depends(access_get)])
async def edit_photo(
        transform: TransformModel,
        photo_id: int = Path(description="The ID of the photo to get", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    new_url = await repository_transforms.get_transform_url(
        photo_id, transform, current_user, db
    )
    if new_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {"url": new_url}


@router.get("/{photo_id}", dependencies=[Depends(access_get)])
async def get_transform_qr(
        photo_id: int = Path(description="The ID of the photo to", gt=0),
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    qrcode_url = await repository_transforms.get_qr_code(photo_id, current_user, db)
    return qrcode_url
