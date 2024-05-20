from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from models.role import RoleFilter
from schemas.role import Role, RoleCreate, RoleUpdate
from crud import role as crud
from database import scoped_session_dependency

router = APIRouter(
    prefix="/roles",
    tags=["Роли"]
)


async def get_role_by_id(role_id: int,
                          session: AsyncSession = Depends(scoped_session_dependency)) -> Role:
    role = await crud.get_role(session=session, role_id=role_id)
    if role is not None:
        return role
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль {role_id} не найдена")


@router.get("/", response_model=list[Role])
async def get_roles(
        role_filter: RoleFilter = FilterDepends(RoleFilter),
        session: AsyncSession = Depends(scoped_session_dependency),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=2),
        order_by: str = Query(default='id'),
) -> list[Role]:
    return await crud.get_roles(session=session, role_filter=role_filter, page=page, size=size, order_by=order_by)


@router.get("/{role_id}/", response_model=Role)
async def get_role(role: Role = Depends(get_role_by_id)):
    return role


@router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
        role_in: RoleCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_role(session=session, role_in=role_in)


@router.patch("/{role_id}/", response_model=Role)
async def update_role(
        role_update: RoleUpdate,
        role: Role = Depends(get_role_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.update_role(session=session,
                                   role=role,
                                   role_update=role_update)


@router.delete("/{role_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
        role: Role = Depends(get_role_by_id),
        session: AsyncSession = Depends(scoped_session_dependency)
) -> None:
    return await crud.delete_role(session=session, role=role)

