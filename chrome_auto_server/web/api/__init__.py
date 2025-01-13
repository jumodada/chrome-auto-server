"""chrome_auto_server API package."""

from fastapi import APIRouter

from chrome_auto_server.web.api import (
    dummy,
    monitoring,
    echo,
    danmaku,
)

api_router = APIRouter()
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(danmaku.router, prefix="/danmaku", tags=["danmaku"])
