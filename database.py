from typing import Optional, TYPE_CHECKING
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship
from sqlalchemy.engine import Engine
from asyncio import current_task


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_async_engine(
    "sqlite+aiosqlite:///db.db", echo=True
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


def get_scoped_session():
    session = async_scoped_session(session_factory=new_session, scopefunc=current_task)
    return session


async def session_dependency() -> AsyncSession:
    async with new_session() as session:
        yield session
        await session.close()


async def scoped_session_dependency() -> AsyncSession:
    session = get_scoped_session()
    yield session
    await session.close()


class Model(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


if TYPE_CHECKING:
    from models.role_user import RoleUser
    from models.customer_car import CustomerCar
    from models.order import Order
    from models.role import Role


class User(SQLAlchemyBaseUserTable[int], Model):
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[Optional[str]]
    is_send_notify: Mapped[bool]
    fullName: Mapped[Optional[str]] = None

    role_user: Mapped["RoleUser"] = relationship(back_populates="user")
    customer_car: Mapped["CustomerCar"] = relationship(back_populates="customer")
    admin_orders: Mapped[list["Order"]] = relationship(back_populates="administrator",
                                                       foreign_keys="Order.administrator_id")
    employee_orders: Mapped[list["Order"]] = relationship(back_populates="employee",
                                                          foreign_keys="Order.employee_id")
    role: Mapped["Role"] = relationship(back_populates="user",
                                        secondary="roleusers",
                                        lazy="joined")



async def get_user_db(session: AsyncSession = Depends(session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
