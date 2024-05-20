from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.brand import BrandFilter
from routes.user import fastapi_users
from schemas.brand import Brand, BrandCreate, BrandUpdate
from crud import brand as crud
from database import scoped_session_dependency, User

router = APIRouter(
    prefix="/brands",
    tags=["Бренды"]
)

current_user = fastapi_users.current_user()

async def get_brand_by_id(brand_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> Brand:
    brand = await crud.get_brand(session=session, brand_id=brand_id)
    if brand is not None:
        return brand
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Бренд {brand_id} не найден")


@router.get("/", response_model=list[Brand])
async def get_brands(
        user: User = Depends(current_user),
        brand_filter: BrandFilter = FilterDepends(BrandFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[Brand]:
    return await crud.get_brands(session=session, brand_filter=brand_filter, page=page, size=size, order_by=order_by)


@router.get("/{brand_id}/", response_model=Brand)
async def get_brand(brand: Brand = Depends(get_brand_by_id)):
    return brand


@router.post("/", response_model=Brand, status_code=status.HTTP_201_CREATED)
async def create_brand(
        brand_in: BrandCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_brand(session=session, brand_in=brand_in)


@router.patch("/{brand_id}/", response_model=Brand)
async def update_brand(
        brand_update: BrandUpdate,
        brand: Brand = Depends(get_brand_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_brand(session=session,
                                   brand=brand,
                                   brand_update=brand_update)


@router.delete("/{brand_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
        brand: Brand = Depends(get_brand_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_brand(session=session, brand=brand)

