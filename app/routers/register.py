from pathlib import Path

from fastapi import APIRouter, HTTPException, status

try:
    from app.auth import auth
    from database.database import db
    from settings.config import config
    from app.schemas import RegisterRequestSchema, RegisterResponseSchema, ErrorSchema
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


register: APIRouter = APIRouter(tags=["Auth"])


@register.post(
    path="/register",
    response_model=RegisterResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to create a new user",
    responses={
        status.HTTP_201_CREATED: {"model": RegisterResponseSchema, "description": "User successfully registered"},
        status.HTTP_409_CONFLICT: {"model": ErrorSchema, "description": "User already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema, "description": "Server error"}
    }
)
async def register_user(new_user: RegisterRequestSchema) -> RegisterResponseSchema:
    if await db.get_user(username=new_user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "Username already exists"})

    hashed_password: str = auth.hash_password(password=new_user.password)
    new_user.password = hashed_password

    if not await db.create_user(new_user=new_user):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "Server error"})

    return RegisterResponseSchema(message="User successfully registered")
