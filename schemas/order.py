import datetime

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import DateTime

from schemas.customer_car import CustomerCar
from schemas.user import User


class OrderBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: int
    start_date: datetime
    end_date: datetime

    @field_serializer('start_date')
    def serialize_date(self, start_date: datetime):
        return start_date.timestamp()

    @field_serializer('end_date')
    def serialize_end_date(self, end_date: datetime):
        return end_date.timestamp()


class OrderCreate(OrderBase):
    administator_id: int
    customer_car_id: int
    employee_id: int


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    administrator: User
    employee: User
    customer_car: CustomerCar


class OrderUpdate(OrderBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    administator_id: int = None
    customer_car_id: int = None
    employee_id: int = None
    status: int = None
    start_date: DateTime = None
    end_date: DateTime = None
