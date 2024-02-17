from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.models import User
from src.database.db import get_db
from src.schemas.users import UserModel, UserResponse, TokenSchema
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/auth', tags=["authentication"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup():
    pass

@router.post("/login", response_model=TokenSchema)
async def login():
    pass

@router.post("/logout")
async def logout():
    pass


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token():
    pass



