from typing import Optional
from pydantic import BaseModel
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class AddUserInfo(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    is_designer: bool = True
    city: str
    description: str
    avatar: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
