from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.dependencies import get_db_session
from chrome_auto_server.db.dao.danmaku_dao import DanmakuDAO
from chrome_auto_server.web.api.danmaku.schemas import DanmakuCreate, DanmakuModel

router = APIRouter()


@router.post("/", response_model=DanmakuModel)
async def create_danmaku(
    danmaku: DanmakuCreate,
    db: AsyncSession = Depends(get_db_session),
) -> DanmakuModel:
    """创建新弹幕."""
    dao = DanmakuDAO(db)
    return await dao.create_danmaku(
        content=danmaku.content,
        author=danmaku.author,
    )


@router.get("/", response_model=List[DanmakuModel])
async def get_danmakus(
    db: AsyncSession = Depends(get_db_session),
) -> List[DanmakuModel]:
    """获取所有弹幕."""
    dao = DanmakuDAO(db)
    return await dao.get_danmakus() 