from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, relationship
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .role_user import RoleUser
    from database import User


class Role(Model):
    name: Mapped[str]

    role_user: Mapped["RoleUser"] = relationship(back_populates="role")
    user: Mapped["User"] = relationship(back_populates="role",
                                        secondary="roleusers")


class RoleFilter(Filter):
    name__like: Optional[str] = None
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Role
