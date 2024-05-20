from typing import Optional
from fastapi_users import schemas

from schemas.role_user import RoleUser


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    is_send_notify: bool


class User(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    is_send_notify: bool
    id: int
    role_user: RoleUser

    class Config:
        orm_mode = True


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    is_send_notify: Optional[bool] = False