from pydantic import BaseModel, ConfigDict

from schemas.brand import Brand


class CarBase(BaseModel):
    model: str


class CarCreate(CarBase):
    brand_id: int


class Car(CarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: Brand


class CarUpdate(CarBase):
    model: str = None
    brand_id: int = None
