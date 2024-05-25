from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import OrderFilter
from routes.user import fastapi_users
from schemas.order import Order, OrderCreate, OrderUpdate
from crud import order as crud
from database import scoped_session_dependency, User

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)

current_active_user = fastapi_users.current_user(active=True)

async def get_order_by_id(order_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> Order:
    order = await crud.get_order(session=session, order_id=order_id)
    if order is not None:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Заказ {order_id} не найден")


@router.get("/", response_model=list[Order])
async def get_orders(
        order_filter: OrderFilter = FilterDepends(OrderFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[Order]:
    return await crud.get_orders(session=session, order_filter=order_filter, page=page, size=size, order_by=order_by)


@router.get("/{order_id}/", response_model=Order)
async def get_order(order: Order = Depends(get_order_by_id),
                    user: User = Depends(current_active_user)):
    if user.id == order.customer_car.customer.id:
        return order
    return None

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
        order_in: OrderCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_order(session=session, order_in=order_in)


@router.patch("/{order_id}/", response_model=Order)
async def update_order(
        order_update: OrderUpdate,
        order: Order = Depends(get_order_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_order(session=session,
                                   order=order,
                                   order_update=order_update)


@router.delete("/{order_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
        order: Order = Depends(get_order_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_order(session=session, order=order)

