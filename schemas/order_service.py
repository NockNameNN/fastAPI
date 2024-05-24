from pydantic import BaseModel, ConfigDict


class OrderServiceBase(BaseModel):
    service_id: int
    order_id: int


class OrderServiceCreate(OrderServiceBase):
    pass


class OrderService(OrderServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderServiceUpdate(OrderServiceBase):
    service_id: int = None
    order_id: int = None
