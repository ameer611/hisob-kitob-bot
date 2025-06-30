from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models, using SQLAlchemy's Declarative system."""
    __abstract__ = True  # This class should not be instantiated directly

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(13), unique=True, nullable=False, index=True)
    tg_id = Column(Integer, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    expenses = relationship('Expense', back_populates='user')

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='expenses')

class WaitingList(Base):
    __tablename__ = 'waiting_list'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(13), unique=True, index=True, nullable=False)