from pathlib import Path

from fastapi import APIRouter, HTTPException, status

try:
    from app.auth import auth
    from database.database import db
    from settings.config import config
    from app.models import UserModel
    from app.schemas import LoginRequestSchema, LoginResponseSchema, ErrorSchema
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


login: APIRouter = APIRouter(tags=["Auth"])


@login.post(
    path="/login",
    response_model=LoginResponseSchema,
    status_code=status.HTTP_200_OK,
    description="Endpoint to login a user",
    responses={
        status.HTTP_200_OK: {"model": LoginResponseSchema, "description": "Logged in successfully"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema, "description": "Incorrect username or password"},
    }
)
async def login_user(user: LoginRequestSchema) -> LoginResponseSchema:
    db_user: UserModel = await db.get_user(username=user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Incorrect username"})

    if not auth.verify_password(password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Incorrect password"})

    token: str = auth.sign_jwt(user_id=db_user.id)
    return LoginResponseSchema(message="Logged in successfully", token=token)
