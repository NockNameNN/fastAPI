from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, relationship
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

# if TYPE_CHECKING:
#     from .order_service import OrderService


class Service(Model):
    name: Mapped[str]
    price: Mapped[int]
    time: Mapped[int]

    # order_services: Mapped[list["OrderService"]] = relationship(back_populates="order")


class ServiceFilter(Filter):
    name__like: Optional[str] = None
    id__gte: Optional[int] = None
    price__gte: Optional[int] = None
    price__lte: Optional[int] = None
    time__gte: Optional[int] = None
    time__lte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Service
