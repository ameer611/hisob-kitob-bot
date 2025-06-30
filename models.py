from datetime import datetime, timezone

from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models, using SQLAlchemy's Declarative system."""
    __abstract__ = True  # This class should not be instantiated directly

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    tg_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    expenses = relationship('Expense', back_populates='user')

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(BigInteger, primary_key=True)
    description = Column(String)
    amount = Column(BigInteger)
    is_active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(BigInteger, ForeignKey('user.id'))

    user = relationship('User', back_populates='expenses')

class WaitingList(Base):
    __tablename__ = 'waiting_list'

    id = Column(BigInteger, primary_key=True)
    phone_number = Column(String, unique=True)