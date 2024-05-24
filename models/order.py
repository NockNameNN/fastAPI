from typing import TYPE_CHECKING, Optional
import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .customer_car import CustomerCar
    from database import User
    from service import Service
    from order_service import OrderService


class Order(Model):
    administrator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    customer_car_id: Mapped[int] = mapped_column(ForeignKey('customercars.id'))
    employee_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    status: Mapped[int]
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    totalTime: Mapped[int]
    totalPrice: Mapped[int]

    customer_car: Mapped["CustomerCar"] = relationship(back_populates="order", lazy='joined')
    administrator: Mapped["User"] = relationship(back_populates="admin_orders",
                                                 foreign_keys=[administrator_id],
                                                 lazy='joined')
    employee: Mapped["User"] = relationship(back_populates="employee_orders",
                                            foreign_keys=[employee_id],
                                            lazy='joined')
    order_service: Mapped["OrderService"] = relationship(back_populates="order")
    services: Mapped[list["Service"]] = relationship(back_populates="orders",
                                                     secondary="orderservices",
                                                     lazy="joined")


class OrderFilter(Filter):
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Order
