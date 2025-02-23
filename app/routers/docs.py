from pathlib import Path

from fastapi import FastAPI, Depends, status
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse

try:
    from app.auth import auth
    from utils.decorators import utils
    from settings.config import config
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


def init_docs(app: FastAPI) -> None:
    @app.get(
        path="/docs",
        response_class=HTMLResponse,
        status_code=status.HTTP_200_OK,
        include_in_schema=False
    )
    async def get_swagger_documentation(_: Depends = Depends(auth.basic)) -> HTMLResponse:
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    @app.get(
        path="/openapi.json",
        response_class=JSONResponse,
        status_code=status.HTTP_200_OK,
        include_in_schema=False
    )
    async def openapi(_: Depends = Depends(auth.basic)) -> JSONResponse:
        return get_openapi(title="Receipt Manager", version="1.0", routes=app.routes)
