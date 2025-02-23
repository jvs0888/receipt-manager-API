from pathlib import Path

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey

try:
    from settings.config import config
    from app.schemas import RegisterRequestSchema, ReceiptRequestSchema
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


Base: DeclarativeMeta = declarative_base()


class UserModel(Base):
    __tablename__: str = "user"

    id: Column = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username: Column = Column(String, unique=True, index=True)
    name: Column = Column(String)
    password: Column = Column(String)
    created_at: Column = Column(DateTime, default=func.now(), onupdate=func.now())

    receipts = relationship(argument="ReceiptModel", back_populates="user")


class ReceiptModel(Base):
    __tablename__: str = "receipt"

    id: Column = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id: Column = Column(Integer, ForeignKey("user.id"), index=True)
    products: Column = Column(JSON)
    payment: Column = Column(JSON)
    total: Column = Column(Float)
    rest: Column = Column(Float)
    created_at: Column = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship(argument="UserModel", back_populates="receipts")
