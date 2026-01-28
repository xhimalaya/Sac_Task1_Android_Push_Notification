from fastapi import APIRouter
from api.routes import subscribe, notify, health

api_router = APIRouter()

api_router.include_router(subscribe.router, prefix="/api")
api_router.include_router(notify.router, prefix="/api")
api_router.include_router(health.router, prefix="/api")
