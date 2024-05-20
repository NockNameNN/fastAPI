from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.role import RoleCreate, RoleUpdate
from models.role import Role, RoleFilter


async def get_roles(
        session: AsyncSession,
        role_filter: RoleFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[Role]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = role_filter.filter(select(Role).order_by(order_by))
    result: Result = await session.execute(stmt)
    roles = result.scalars().all()

    return list(roles[offset_min:offset_max])


async def get_role(session: AsyncSession, role_id: int) -> Role | None:
    return await session.get(Role, role_id)


async def create_role(session: AsyncSession, role_in: RoleCreate) -> Role:
    role = Role(**role_in.model_dump())
    session.add(role)
    await session.commit()
    return role


async def update_role(
        session: AsyncSession,
        role: Role,
        role_update: RoleUpdate) -> Role:
    for name, value in role_update.model_dump(exclude_unset=True).items():
        setattr(role, name, value)
    await session.commit()
    return role


async def delete_role(session: AsyncSession, role: Role) -> None:
    await session.delete(role)
    await session.commit()

