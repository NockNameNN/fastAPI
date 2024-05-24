from pydantic import BaseModel, ConfigDict

from schemas.car import Car
from schemas.user import UserInformation, User


class CustomerCarBase(BaseModel):
    year: int
    number: str


class CustomerCarCreate(CustomerCarBase):
    car_id: int
    customer_id: int


class CustomerCar(CustomerCarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car: Car
    customer: UserInformation


class CustomerCarUpdate(CustomerCarBase):
    car_id: int = None
    customer_id: int = None
    year: int = None
    number: str = None
