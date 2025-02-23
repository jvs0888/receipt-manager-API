from app.routers.docs import init_docs
from app.routers.register import register
from app.routers.login import login
from app.routers.receipt import receipt

ROUTERS: list = [
    register,
    login,
    receipt
]
