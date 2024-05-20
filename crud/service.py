from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.service import ServiceCreate, ServiceUpdate
from models.service import Service, ServiceFilter


async def get_services(
        session: AsyncSession,
        service_filter: ServiceFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[Service]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = service_filter.filter(select(Service).order_by(order_by))
    result: Result = await session.execute(stmt)
    services = result.scalars().all()

    return list(services[offset_min:offset_max])


async def get_service(session: AsyncSession, service_id: int) -> Service | None:
    return await session.get(Service, service_id)


async def create_service(session: AsyncSession, service_in: ServiceCreate) -> Service:
    service = Service(**service_in.model_dump())
    session.add(service)
    await session.commit()
    return service


async def update_service(
        session: AsyncSession,
        service: Service,
        service_update: ServiceUpdate) -> Service:
    for name, value in service_update.model_dump(exclude_unset=True).items():
        setattr(service, name, value)
    await session.commit()
    return service


async def delete_service(session: AsyncSession, service: Service) -> None:
    await session.delete(service)
    await session.commit()

