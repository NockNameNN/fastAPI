from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from schemas.customer_car import CustomerCarCreate, CustomerCarUpdate
from models.customer_car import CustomerCar, CustomerCarFilter


async def get_customer_cars(
        session: AsyncSession,
        customer_car_filter: CustomerCarFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[CustomerCar]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = customer_car_filter.filter(select(CustomerCar).order_by(order_by))

    result: Result = await session.execute(stmt)
    customer_cars = result.scalars().all()

    return list(customer_cars[offset_min:offset_max])


async def get_customer_car(session: AsyncSession, customer_car_id: int) -> CustomerCar | None:
    return await session.get(CustomerCar, customer_car_id)


async def create_customer_car(session: AsyncSession, customer_car_in: CustomerCarCreate) -> CustomerCar:
    customer_car = CustomerCar(**customer_car_in.model_dump())
    session.add(customer_car)
    await session.commit()
    return customer_car


async def update_customer_car(
        session: AsyncSession,
        customer_car: CustomerCar,
        customer_car_update: CustomerCarUpdate) -> CustomerCar:
    for name, value in customer_car_update.model_dump(exclude_unset=True).items():
        setattr(customer_car, name, value)
    await session.commit()
    return customer_car


async def delete_customer_car(session: AsyncSession, customer_car: CustomerCar) -> None:
    await session.delete(customer_car)
    await session.commit()

