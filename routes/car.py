from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.car import CarFilter
from schemas.car import Car, CarCreate, CarUpdate
from crud import car as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/cars",
    tags=["Автомобили"]
)


async def get_car_by_id(car_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> Car:
    car = await crud.get_car(session=session, car_id=car_id)
    if car is not None:
        return car
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Автомобиль {car_id} не найден")


@router.get("/", response_model=list[Car])
async def get_cars(
        car_filter: CarFilter = FilterDepends(CarFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[Car]:
    return await crud.get_cars(session=session, car_filter=car_filter, page=page, size=size, order_by=order_by)


@router.get("/{car_id}/", response_model=Car)
async def get_car(car: Car = Depends(get_car_by_id)):
    return car


@router.post("/", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car(
        car_in: CarCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_car(session=session, car_in=car_in)


@router.patch("/{car_id}/", response_model=Car)
async def update_car(
        car_update: CarUpdate,
        car: Car = Depends(get_car_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_car(session=session,
                                   car=car,
                                   car_update=car_update)


@router.delete("/{car_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
        car: Car = Depends(get_car_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_car(session=session, car=car)

