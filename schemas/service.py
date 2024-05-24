from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ServiceBase(BaseModel):
    name: str
    price: int
    time: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    minValue: int | None = None
    format: str | None = None
    second: int | None = None

    @field_validator('minValue')
    def validate_min_value(cls, v, values) -> int:
        return values.data["price"] * 100

    @field_validator('format')
    def validate_format(cls, v, values) -> str:
        return f'{values.data["price"]} руб.'

    @field_validator('second')
    def validate_second(cls, v, values) -> int:
        return values.data["time"] * 60


class ServiceUpdate(ServiceBase):
    name: str | None = None
    price: int | None = None
    time: int | None = None
