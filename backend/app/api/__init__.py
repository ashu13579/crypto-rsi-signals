"""API routes"""
from fastapi import APIRouter
from .signals import router as signals_router
from .market import router as market_router
from .settings import router as settings_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(signals_router, prefix="/signals", tags=["signals"])
api_router.include_router(market_router, prefix="/market", tags=["market"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
