import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field

from schemas.customer_car import CustomerCar
from schemas.service import Service
from schemas.user import UserInformation


class OrderBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: int

class OrderCreate(OrderBase):
    administrator_id: int
    customer_car_id: int
    employee_id: int


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    services: list[Service] = Field(exclude=True)
    totalPrice: int | None = None
    totalTime: int | None = None
    start_date: datetime
    end_date: datetime
    administrator: UserInformation
    employee: UserInformation
    customer_car: CustomerCar

    @field_validator('totalPrice')
    def validate_total_price(cls, v, values):
        return sum(service.price for service in values.data["services"])

    @field_validator('totalTime')
    def validate_total_time(cls, v, values):
        return sum(service.time for service in values.data["services"])

    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        return values.data["start_date"] + datetime.timedelta(minutes=sum(service.time for service in values.data["services"]))



class OrderUpdate(OrderBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: int = None
