from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role, User


class UserModel(BaseModel):
    pass


class UserResponse(BaseModel):
    pass


class TokenSchema(BaseModel):
    pass


class UserUpdateModel(BaseModel):
    pass
