import typing as t
from datetime import datetime, date

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class _BaseUserSchema(BaseModel):
    username: str
    password: str


class RegisterRequestSchema(_BaseUserSchema):
    name: str


class LoginRequestSchema(_BaseUserSchema):
    pass


class ProductRequestSchema(BaseModel):
    name: str
    price: float
    quantity: int
    total: t.Optional[float] = None


class PaymentRequestSchema(BaseModel):
    payment_type: str
    amount: float


class ReceiptRequestSchema(BaseModel):
    products: list[ProductRequestSchema]
    payment: PaymentRequestSchema


class ReceiptListRequestSchema(BaseModel):
    start_date: t.Optional[date] = None
    end_date: t.Optional[date] = None
    min_total: t.Optional[float] = None
    payment_type: t.Optional[str] = None
    page: int = 1
    page_size: int = 10

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_date(cls, value: t.Optional[str]) -> t.Optional[str]:
        if value is None:
            return value

        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Invalid date"})
