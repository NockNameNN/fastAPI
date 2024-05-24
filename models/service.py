from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, relationship
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .order_service import OrderService
    from .order import Order


class Service(Model):
    name: Mapped[str]
    price: Mapped[int]
    time: Mapped[int]
    minValue: Mapped[Optional[int]] = None
    format: Mapped[Optional[str]] = None
    second: Mapped[Optional[int]] = None

    order_service: Mapped["OrderService"] = relationship(back_populates="service")
    orders: Mapped[list["Order"]] = relationship(back_populates="services",
                                                 secondary="orderservices")


class ServiceFilter(Filter):
    name__like: Optional[str] = None
    id__gte: Optional[int] = None
    price__gte: Optional[int] = None
    price__lte: Optional[int] = None
    time__gte: Optional[int] = None
    time__lte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Service
