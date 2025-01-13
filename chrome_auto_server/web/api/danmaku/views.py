from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.dependencies import get_db_session
from chrome_auto_server.db.dao.danmaku_dao import DanmakuDAO
from chrome_auto_server.web.api.danmaku.schemas import DanmakuCreate, DanmakuModel, DanmakuResponse

router = APIRouter()


@router.post("/create-danmaku", response_model=DanmakuResponse)
async def create_danmaku(
    danmaku: DanmakuCreate,
    db: AsyncSession = Depends(get_db_session),
) -> DanmakuResponse:
    print(danmaku)
    try:
        dao = DanmakuDAO(db)
        created_danmaku = await dao.create_danmaku(
            content=danmaku.content,
            author=danmaku.author,
        )
        return DanmakuResponse(
            success=True,
            message="弹幕创建成功",
            data=created_danmaku
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"创建弹幕失败: {str(e)}"
        )


@router.get("/get-danmakus", response_model=List[DanmakuModel])
async def get_danmakus(
    db: AsyncSession = Depends(get_db_session),
) -> List[DanmakuModel]:
    print("获取所有弹幕")
    dao = DanmakuDAO(db)
    print('开始获取弹幕')
    return await dao.get_danmakus() 
