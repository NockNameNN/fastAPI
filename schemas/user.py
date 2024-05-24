from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, field_validator, Field

from schemas.role import Role


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
    role: Role


class UserInformation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    patronymic: Optional[str] = Field(None, exclude=True)
    id: int
    fullName: str | None = None
    email: str

    @field_validator('fullName')
    def validate_full_name(cls, v, values) -> str:
        return values.data["first_name"] + ' ' + values.data["last_name"] + ' ' + values.data["patronymic"]

class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    is_send_notify: Optional[bool] = False