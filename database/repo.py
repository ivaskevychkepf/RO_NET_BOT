from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from datetime import datetime, timedelta

async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str = None, full_name: str = None):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            balance=0.0,
            tariff="Стартовий"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def update_user_balance(db: AsyncSession, telegram_id: int, new_balance: float):
    await db.execute(
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(balance=new_balance)
    )
    await db.commit()

from .models import Ticket

async def create_ticket(db: AsyncSession, telegram_id: int, ticket_type: str, description: str = None):
    ticket = Ticket(
        telegram_id=telegram_id,
        ticket_type=ticket_type,
        description=description,
        status="Нова"
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

from sqlalchemy import update

async def change_user_tariff(db: AsyncSession, telegram_id: int, new_tariff: str, price: float):
    await db.execute(
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(
            tariff=new_tariff,
            balance=User.balance - price
        )
    )
    await db.commit()

async def pause_internet(db, telegram_id: int, days: int):
    end_date = datetime.utcnow() + timedelta(days=days)

    await db.execute(
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(
            internet_paused=True,
            pause_until=end_date
        )
    )
    await db.commit()

    return end_date


async def cancel_pause(db, telegram_id: int):
    await db.execute(
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(
            internet_paused=False,
            pause_until=None
        )
    )
    await db.commit()


async def get_user(db, telegram_id: int):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def add_balance(db, telegram_id: int, amount: int):
    result = await db.execute(
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(balance=User.balance + amount)
    )
    await db.commit()

from sqlalchemy import select
from database.models import Payment
from datetime import datetime


async def create_payment(db, telegram_id: int, amount: float, invoice_id: str):
    payment = Payment(
        telegram_id=telegram_id,
        amount=amount,
        invoice_id=invoice_id,
        status="pending"
    )
    db.add(payment)
    await db.commit()
    return payment


async def update_payment_status(db, invoice_id: str, status: str):
    result = await db.execute(
        select(Payment).where(Payment.invoice_id == invoice_id)
    )
    payment = result.scalars().first()

    if payment:
        payment.status = status
        await db.commit()

    return payment


async def get_user_payments(db, telegram_id: int):
    result = await db.execute(
        select(Payment)
        .where(Payment.telegram_id == telegram_id)
        .order_by(Payment.created_at.desc())
    )
    return result.scalars().all()