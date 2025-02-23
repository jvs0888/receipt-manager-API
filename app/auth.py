import time
import jwt
import bcrypt
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

try:
    from settings.config import config
    from app.schemas import ReceiptRequestSchema
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


class Auth:
    security: HTTPBasic = HTTPBasic()
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def basic(credentials: HTTPBasicCredentials = Depends(security)) -> None:
        if credentials.username != config.ADMIN_USER or credentials.password != config.ADMIN_PASS:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        payload: dict = {
            "id": user_id,
            "exp": time.time() + 3600
        }
        return jwt.encode(payload=payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

    @staticmethod
    def verify_jwt(token: str = Depends(oauth2_scheme)) -> dict:
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail={"error": "Token not provided"})

        try:
            return jwt.decode(jwt=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Token has expired"})
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})

    @staticmethod
    def hash_password(password: str) -> str:
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


auth: Auth = Auth()
