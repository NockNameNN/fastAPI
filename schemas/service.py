from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    name: str
    price: int
    time: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ServiceUpdate(ServiceBase):
    name: str | None = None
    price: int | None = None
    time: int | None = None
