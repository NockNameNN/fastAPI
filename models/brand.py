from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, relationship
from fastapi_filter.contrib.sqlalchemy import Filter
from database import Model

if TYPE_CHECKING:
    from .car import Car


class Brand(Model):
    name: Mapped[str]

    cars: Mapped[list["Car"]] = relationship(back_populates="brand")


class BrandFilter(Filter):
    name__like: Optional[str] = None
    id__gte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Brand
