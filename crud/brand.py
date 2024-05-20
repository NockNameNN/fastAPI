from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.brand import BrandCreate, BrandUpdate
from models.brand import Brand, BrandFilter


async def get_brands(
        session: AsyncSession,
        brand_filter: BrandFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[Brand]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = brand_filter.filter(select(Brand).order_by(order_by))
    result: Result = await session.execute(stmt)
    brands = result.scalars().all()

    return list(brands[offset_min:offset_max])


async def get_brand(session: AsyncSession, brand_id: int) -> Brand | None:
    return await session.get(Brand, brand_id)


async def create_brand(session: AsyncSession, brand_in: BrandCreate) -> Brand:
    brand = Brand(**brand_in.model_dump())
    session.add(brand)
    await session.commit()
    return brand


async def update_brand(
        session: AsyncSession,
        brand: Brand,
        brand_update: BrandUpdate) -> Brand:
    for name, value in brand_update.model_dump(exclude_unset=True).items():
        setattr(brand, name, value)
    await session.commit()
    return brand


async def delete_brand(session: AsyncSession, brand: Brand) -> None:
    await session.delete(brand)
    await session.commit()

