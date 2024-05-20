from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .car import Car
    from database import User


class CustomerCar(Model):
    year: Mapped[int]
    number: Mapped[str]
    car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))
    customer_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    car: Mapped["Car"] = relationship(back_populates="customer_car", lazy='joined')
    customer: Mapped["User"] = relationship(back_populates="customer_car", lazy='joined')


class CustomerCarFilter(Filter):
    year__gte: Optional[int] = None
    number__like: Optional[str] = None
    car_id__gte: Optional[int] = None
    car_id__lte: Optional[int] = None
    user_id__gte: Optional[int] = None
    user_id__lte: Optional[str] = None
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = CustomerCar
