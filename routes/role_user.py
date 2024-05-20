from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.role_user import RoleUserFilter
from schemas.role_user import RoleUser, RoleUserCreate, RoleUserUpdate
from crud import role_user as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/role-users",
    tags=["Роли пользователей"]
)


async def get_role_user_by_id(role_user_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> RoleUser:
    role_user = await crud.get_role_user(session=session, role_user_id=role_user_id)
    if role_user is not None:
        return role_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль {role_user_id} не найдена")


@router.get("/", response_model=list[RoleUser])
async def get_role_users(
        role_user_filter: RoleUserFilter = FilterDepends(RoleUserFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[RoleUser]:
    return await crud.get_role_users(session=session, role_user_filter=role_user_filter, page=page, size=size, order_by=order_by)


@router.get("/{role_user_id}/", response_model=RoleUser)
async def get_role_user(role_user: RoleUser = Depends(get_role_user_by_id)):
    return role_user


@router.post("/", response_model=RoleUser, status_code=status.HTTP_201_CREATED)
async def create_role_user(
        role_user_in: RoleUserCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_role_user(session=session, role_user_in=role_user_in)


@router.patch("/{role_user_id}/", response_model=RoleUser)
async def update_role_user(
        role_user_update: RoleUserUpdate,
        role_user: RoleUser = Depends(get_role_user_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_role_user(session=session,
                                   role_user=role_user,
                                   role_user_update=role_user_update)


@router.delete("/{role_user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_user(
        role_user: RoleUser = Depends(get_role_user_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_role_user(session=session, role_user=role_user)

