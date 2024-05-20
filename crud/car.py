from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.car import CarCreate, CarUpdate
from models.car import Car, CarFilter


async def get_cars(
        session: AsyncSession,
        car_filter: CarFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[Car]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = car_filter.filter(select(Car).order_by(order_by))

    result: Result = await session.execute(stmt)
    cars = result.scalars().all()

    return list(cars[offset_min:offset_max])


async def get_car(session: AsyncSession, car_id: int) -> Car | None:
    return await session.get(Car, car_id)


async def create_car(session: AsyncSession, car_in: CarCreate) -> Car:
    car = Car(**car_in.model_dump())
    session.add(car)
    await session.commit()
    return car


async def update_car(
        session: AsyncSession,
        car: Car,
        car_update: CarUpdate) -> Car:
    for name, value in car_update.model_dump(exclude_unset=True).items():
        setattr(car, name, value)
    await session.commit()
    return car


async def delete_car(session: AsyncSession, car: Car) -> None:
    await session.delete(car)
    await session.commit()

