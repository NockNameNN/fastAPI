from pydantic import BaseModel


class OrderServiceBase(BaseModel):
    name: str


class OrderServiceCreate(OrderServiceBase):
    pass


class OrderService(OrderServiceBase):
    id: int

    class Config:
        orm_mode = True