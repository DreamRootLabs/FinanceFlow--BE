from fastapi import APIRouter

from .health import health_router
from .auth import router as auth_router
from .categories import router as categories_router
from .transactions import router as transactions_router
from .reports import router as reports_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(transactions_router)
api_router.include_router(reports_router)