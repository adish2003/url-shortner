from fastapi import APIRouter

from app.api.routes.root import router as root_router
from app.api.routes.url_routes import router as url_router

api_router = APIRouter()
api_router.include_router(root_router)
api_router.include_router(url_router)
