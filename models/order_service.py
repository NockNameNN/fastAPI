from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from order import Order
    from service import Service


class OrderService(Model):
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))

    service: Mapped["Service"] = relationship(back_populates="order_service")
    order: Mapped["Order"] = relationship(back_populates="order_service")

class OrderServiceFilter(Filter):
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = OrderService
