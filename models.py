from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    phone_number = Column(String, unique=True)
    tg_id = Column(String, unique=True)
    created_at = Column(DateTime)

    expenses = relationship('Expense', back_populates='user')

class Expense(Base):
    __tablename__ = 'expense'

    id = Column(BigInteger, primary_key=True)
    description = Column(String)
    amount = Column(BigInteger)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey('user.id'))

    user = relationship('User', back_populates='expenses')

class WaitingList(Base):
    __tablename__ = 'waiting_list'

    id = Column(BigInteger, primary_key=True)
    phone_number = Column(String, unique=True)