from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from database import User


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user

