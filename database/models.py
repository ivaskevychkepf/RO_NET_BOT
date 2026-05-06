from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    username = Column(String(100))
    full_name = Column(String(200))
    phone = Column(String(20))
    address = Column(String(300))

    balance = Column(Float, default=0.0)
    tariff = Column(String(100), default="Стартовий")

    is_active = Column(Boolean, default=True)

    # 🔥 НОВЕ
    internet_paused = Column(Boolean, default=False)
    pause_until = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.telegram_id}>"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    ticket_type = Column(String(100), nullable=False)
    description = Column(String(1000))
    status = Column(String(50), default="Нова")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Ticket {self.id} - {self.status}>"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, index=True)

    amount = Column(Float)
    status = Column(String, default="pending")
    provider = Column(String, default="mono")

    invoice_id = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)