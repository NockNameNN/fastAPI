from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.service import ServiceFilter
from schemas.service import Service, ServiceCreate, ServiceUpdate
from crud import service as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/services",
    tags=["Сервисы"]
)


async def get_service_by_id(service_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> Service:
    service = await crud.get_service(session=session, service_id=service_id)
    if service is not None:
        return service
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Сервис {service_id} не найден")


@router.get("/", response_model=list[Service])
async def get_services(
        service_filter: ServiceFilter = FilterDepends(ServiceFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[Service]:
    return await crud.get_services(session=session, service_filter=service_filter, page=page, size=size, order_by=order_by)


@router.get("/{service_id}/", response_model=Service)
async def get_service(service: Service = Depends(get_service_by_id)):
    return service


@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(
        service_in: ServiceCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_service(session=session, service_in=service_in)


@router.patch("/{service_id}/", response_model=Service)
async def update_service(
        service_update: ServiceUpdate,
        service: Service = Depends(get_service_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_service(session=session,
                                   service=service,
                                   service_update=service_update)


@router.delete("/{service_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
        service: Service = Depends(get_service_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_service(session=session, service=service)

