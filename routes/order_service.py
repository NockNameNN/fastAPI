from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.order_service import OrderServiceFilter
from schemas.order_service import OrderService, OrderServiceCreate, OrderServiceUpdate
from crud import order_service as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/order_services",
    tags=["Сервисы заказов"]
)


async def get_order_service_by_id(order_service_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> OrderService:
    order_service = await crud.get_order_service(session=session, order_service_id=order_service_id)
    if order_service is not None:
        return order_service
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Сервис заказа {order_service_id} не найден")


@router.get("/", response_model=list[OrderService])
async def get_order_services(
        order_service_filter: OrderServiceFilter = FilterDepends(OrderServiceFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[OrderService]:
    return await crud.get_order_services(session=session, order_service_filter=order_service_filter, page=page, size=size, order_by=order_by)


@router.get("/{order_service_id}/", response_model=OrderService)
async def get_order_service(order_service: OrderService = Depends(get_order_service_by_id)):
    return order_service


@router.post("/", response_model=OrderService, status_code=status.HTTP_201_CREATED)
async def create_order_service(
        order_service_in: OrderServiceCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_order_service(session=session, order_service_in=order_service_in)


@router.patch("/{order_service_id}/", response_model=OrderService)
async def update_order_service(
        order_service_update: OrderServiceUpdate,
        order_service: OrderService = Depends(get_order_service_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_order_service(session=session,
                                   order_service=order_service,
                                   order_service_update=order_service_update)


@router.delete("/{order_service_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_service(
        order_service: OrderService = Depends(get_order_service_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_order_service(session=session, order_service=order_service)

