from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.order_service import OrderServiceCreate, OrderServiceUpdate
from models.order_service import OrderService, OrderServiceFilter


async def get_order_services(
        session: AsyncSession,
        order_service_filter: OrderServiceFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[OrderService]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = order_service_filter.filter(select(OrderService).order_by(order_by))

    result: Result = await session.execute(stmt)
    order_services = result.scalars().all()

    return list(order_services[offset_min:offset_max])


async def get_order_service(session: AsyncSession, order_service_id: int) -> OrderService | None:
    return await session.get(OrderService, order_service_id)


async def create_order_service(session: AsyncSession, order_service_in: OrderServiceCreate) -> OrderService:
    order_service = OrderService(**order_service_in.model_dump())
    session.add(order_service)
    await session.commit()
    return order_service


async def update_order_service(
        session: AsyncSession,
        order_service: OrderService,
        order_service_update: OrderServiceUpdate) -> OrderService:
    for name, value in order_service_update.model_dump(exclude_unset=True).items():
        setattr(order_service, name, value)
    await session.commit()
    return order_service


async def delete_order_service(session: AsyncSession, order_service: OrderService) -> None:
    await session.delete(order_service)
    await session.commit()

