from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .brand import Brand
    from .customer_car import CustomerCar


class Car(Model):
    model: Mapped[str]
    brand_id: Mapped[int] = mapped_column(ForeignKey('brands.id'))

    brand: Mapped["Brand"] = relationship(back_populates="cars", lazy='joined')
    customer_car: Mapped["CustomerCar"] = relationship(back_populates="car")


class CarFilter(Filter):
    model__like: Optional[str] = None
    brand_id__gte: Optional[int] = None
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Car
