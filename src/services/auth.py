from typing import Optional

import redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
    )


    def verify_password() -> bool:
        pass


    def get_password_hash() -> str:
        pass

    async def create_access_token():
        pass


    async def create_refresh_token():
        pass


    async def decode_refresh_token() -> str:
        pass

auth_service = Auth()