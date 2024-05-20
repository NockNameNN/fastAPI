from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.role_user import RoleUserCreate, RoleUserUpdate
from models.role_user import RoleUser, RoleUserFilter


async def get_role_users(
        session: AsyncSession,
        role_user_filter: RoleUserFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[RoleUser]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = role_user_filter.filter(select(RoleUser).order_by(order_by))

    result: Result = await session.execute(stmt)
    role_users = result.scalars().all()

    return list(role_users[offset_min:offset_max])


async def get_role_user(session: AsyncSession, role_user_id: int) -> RoleUser | None:
    return await session.get(RoleUser, role_user_id)


async def create_role_user(session: AsyncSession, role_user_in: RoleUserCreate) -> RoleUser:
    role_user = RoleUser(**role_user_in.model_dump())
    session.add(role_user)
    await session.commit()
    return role_user


async def update_role_user(
        session: AsyncSession,
        role_user: RoleUser,
        role_user_update: RoleUserUpdate) -> RoleUser:
    for name, value in role_user_update.model_dump(exclude_unset=True).items():
        setattr(role_user, name, value)
    await session.commit()
    return role_user


async def delete_role_user(session: AsyncSession, role_user: RoleUser) -> None:
    await session.delete(role_user)
    await session.commit()

