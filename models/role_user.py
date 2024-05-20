from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .role import Role
    from database import User


class RoleUser(Model):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

    role: Mapped["Role"] = relationship(back_populates="role_user")
    user: Mapped["User"] = relationship(back_populates="role_user")


class RoleUserFilter(Filter):
    user_id__gte: Optional[str] = None
    role_id__gte: Optional[int] = None
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = RoleUser
