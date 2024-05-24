import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.order import OrderCreate, OrderUpdate
from models.order import Order, OrderFilter
from tasks.email import send_email


async def get_orders(
        session: AsyncSession,
        order_filter: OrderFilter,
        page: int,
        size: int,
        order_by: str,
) -> list[Order]:
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = order_filter.filter(select(Order).order_by(order_by))

    result: Result = await session.execute(stmt)
    orders = result.unique().scalars().all()

    return list(orders[offset_min:offset_max])


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    return await session.get(Order, order_id)


async def create_order(session: AsyncSession, order_in: OrderCreate) -> Order:
    order = Order(**order_in.model_dump())
    session.add(order)
    await session.commit()
    return order


async def update_order(
        session: AsyncSession,
        order: Order,
        order_update: OrderUpdate) -> Order:
    for name, value in order_update.model_dump(exclude_unset=True).items():
        setattr(order, name, value)

    if (order.status == 1) and (order.customer_car.customer.is_send_notify == 1):
        customer_email = order.customer_car.customer.email
        subject = "Order Completed"
        body = f"Your order with ID {order.id} has been completed."
        send_email(customer_email, subject, body)

    await session.commit()

    return order


async def delete_order(session: AsyncSession, order: Order) -> None:
    await session.delete(order)
    await session.commit()

