from fastapi.routing import APIRouter

from chrome_auto_server.web.api import docs, dummy, echo, monitoring, danmaku, redis

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(danmaku.router, prefix="/danmaku", tags=["danmaku"])
