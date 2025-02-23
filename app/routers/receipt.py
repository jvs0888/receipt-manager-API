from pathlib import Path

from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, Query, HTTPException, Request, status

try:
    from app.auth import auth
    from database.database import db
    from settings.config import config
    from app.templates import templates
    from app.schemas import (
        ReceiptRequestSchema,
        BaseReceiptResponseSchema,
        ReceiptResponseSchema,
        ReceiptListRequestSchema,
        ReceiptListResponseSchema,
        ErrorSchema
    )
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


receipt: APIRouter = APIRouter(tags=["Receipt"])


@receipt.post(
    path="/receipt/create",
    response_model=BaseReceiptResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to create a new receipt",
    responses={
        status.HTTP_201_CREATED: {"model": BaseReceiptResponseSchema, "description": "Receipt successfully created"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Insufficient funds"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Not authenticated"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema, "description": "Server error"}
    }
)
async def create_receipt(receipt: ReceiptRequestSchema, user: dict = Depends(auth.verify_jwt)) -> BaseReceiptResponseSchema:
    total = float()
    for product in receipt.products:
        total_price: float = product.price * product.quantity
        total += total_price
        product.total = round(total_price, 2)

    rest: float = receipt.payment.amount - total
    if rest < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Not enough money"})

    new_receipt: ReceiptResponseSchema = ReceiptResponseSchema(
        user_id=user.get("id"),
        products=receipt.products,
        payment=receipt.payment,
        total=round(total, 2),
        rest=round(rest, 2)
    )

    base_receipt: BaseReceiptResponseSchema = await db.create_receipt(new_receipt=new_receipt)
    if not base_receipt:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "Server error"})

    return base_receipt


@receipt.get(
    path="/receipt/list",
    response_model=ReceiptListResponseSchema,
    status_code=status.HTTP_200_OK,
    description="Endpoint to get a list of receipts using filters",
    responses={
        status.HTTP_200_OK: {"model": ReceiptListResponseSchema, "description": "List of receipts successfully retrieved"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema, "description": "Invalid date"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Incorrect username or password"},
    }
)
async def get_receipt_list(filters: ReceiptListRequestSchema = Depends(),
                           user: dict = Depends(auth.verify_jwt)) -> ReceiptResponseSchema:
    receipts: list[BaseReceiptResponseSchema] = await db.get_filtered_receipts(user_id=user.get("id"), filters=filters)
    count: int = len(receipts) if receipts else 0

    return ReceiptListResponseSchema(count=count, receipts=receipts)


@receipt.get(
    path="/receipt/{receipt_id}",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Endpoint to get a receipt by ID",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema, "description": "Receipt not found"},
    }
)
async def get_receipt(request: Request,
                      receipt_id: int,
                      max_characters: int = Query(default=30, alias="max_characters")) -> HTMLResponse:
    receipt: BaseReceiptResponseSchema = await db.get_receipt(receipt_id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Receipt not found"})

    return templates.TemplateResponse("receipt_template.html", {
        "request": request,
        "receipt_width": max_characters * 8,
        **receipt.model_dump()
    })
