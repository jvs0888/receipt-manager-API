import typing as t
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel

try:
    from app.schemas.request import ProductRequestSchema, PaymentRequestSchema
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


class _BaseResponseSchema(BaseModel):
    message: str


class RegisterResponseSchema(_BaseResponseSchema):
    pass


class LoginResponseSchema(_BaseResponseSchema):
    token: str


class BaseReceiptResponseSchema(BaseModel):
    id: t.Optional[int] = None
    products: list[ProductRequestSchema]
    payment: PaymentRequestSchema
    total: float
    rest: float
    created_at: t.Optional[datetime] = None

    class Config:
        from_attributes: bool = True


class ReceiptResponseSchema(BaseReceiptResponseSchema):
    user_id: t.Optional[int] = None


class ReceiptListResponseSchema(BaseModel):
    count: int
    receipts: list[BaseReceiptResponseSchema]


class ErrorSchema(BaseModel):
    error: str
