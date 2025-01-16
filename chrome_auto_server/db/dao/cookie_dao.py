from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.models.cookie_model import CookieModel

class CookieDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_cookie(
        self,
        domain: str,
        username: str,
        cookie_data: dict,
    ) -> CookieModel:
        """创建或更新Cookie记录"""
        query = select(CookieModel).where(
            CookieModel.domain == domain,
            CookieModel.username == username
        )
        result = await self.session.execute(query)
        existing_cookie = result.scalar_one_or_none()
        print(existing_cookie)
        if existing_cookie:
            await self.session.flush()
            return existing_cookie
        
        # 创建新记录
        new_cookie = CookieModel(
            domain=domain,
            username=username,
            cookie_data=cookie_data,
        )
        self.session.add(new_cookie)
        await self.session.flush()
        return new_cookie

    async def get_cookie(
        self,
        domain: str,
        username: str,
    ) -> Optional[CookieModel]:
        """获取指定域名和用户名的Cookie"""
        query = select(CookieModel).where(
            CookieModel.domain == domain,
            CookieModel.username == username
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() 