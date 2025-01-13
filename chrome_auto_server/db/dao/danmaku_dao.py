from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.models.danmaku import DanmakuModel


class DanmakuDAO:
    """Class for accessing danmaku table."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_danmaku(
        self,
        content: str,
        author: str,
    ) -> DanmakuModel:
        """创建新弹幕."""
        new_danmaku = DanmakuModel(
            content=content,
            author=author,
        )
        self.session.add(new_danmaku)
        await self.session.commit()
        return new_danmaku

    async def get_danmakus(self) -> List[DanmakuModel]:
        """获取所有弹幕."""
        query = select(DanmakuModel).order_by(DanmakuModel.created_at.desc())
        rows = await self.session.execute(query)
        return list(rows.scalars().all()) 