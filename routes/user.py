from fastapi import APIRouter, status, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user as crud
from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import scoped_session_dependency
from schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(User, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(User, UserUpdate),
    prefix="/users",
    tags=["Пользователи"],
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(scoped_session_dependency)):
    return await crud.create_user(session=session, user_in=user_in)
