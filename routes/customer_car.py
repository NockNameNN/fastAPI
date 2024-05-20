from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.customer_car import CustomerCarFilter
from schemas.customer_car import CustomerCar, CustomerCarCreate, CustomerCarUpdate
from crud import customer_car as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/customer_cars",
    tags=["Автомобили клиентов"]
)


async def get_customer_car_by_id(customer_car_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> CustomerCar:
    customer_car = await crud.get_customer_car(session=session, customer_car_id=customer_car_id)
    if customer_car is not None:
        return customer_car
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Автомобиль клиента {customer_car_id} не найден")


@router.get("/", response_model=list[CustomerCar])
async def get_customer_cars(
        customer_car_filter: CustomerCarFilter = FilterDepends(CustomerCarFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[CustomerCar]:
    return await crud.get_customer_cars(session=session, customer_car_filter=customer_car_filter, page=page, size=size, order_by=order_by)


@router.get("/{customer_car_id}/", response_model=CustomerCar)
async def get_customer_car(customer_car: CustomerCar = Depends(get_customer_car_by_id)):
    return customer_car


@router.post("/", response_model=CustomerCar, status_code=status.HTTP_201_CREATED)
async def create_customer_car(
        customer_car_in: CustomerCarCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_customer_car(session=session, customer_car_in=customer_car_in)


@router.patch("/{customer_car_id}/", response_model=CustomerCar)
async def update_customer_car(
        customer_car_update: CustomerCarUpdate,
        customer_car: CustomerCar = Depends(get_customer_car_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_customer_car(session=session,
                                   customer_car=customer_car,
                                   customer_car_update=customer_car_update)


@router.delete("/{customer_car_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_car(
        customer_car: CustomerCar = Depends(get_customer_car_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_customer_car(session=session, customer_car=customer_car)

