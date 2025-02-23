from pathlib import Path
from fastapi import FastAPI

try:
    from database.database import db
    from utils.decorators import utils
    from settings.config import config
    from app.routers import ROUTERS, init_docs
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


@utils.exception
def init_app() -> FastAPI:
    app: FastAPI = FastAPI(lifespan=db.init, openapi_url=None)
    init_docs(app=app)

    for router in ROUTERS:
        app.include_router(router=router)

    return app
