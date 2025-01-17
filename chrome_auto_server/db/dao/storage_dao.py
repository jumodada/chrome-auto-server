from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.models.storage_model import StorageModel

class StorageDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_storage(
        self,
        domain: str,
        username: str,
        storage_data: dict,
    ) -> StorageModel:
        query = select(StorageModel).where(
            StorageModel.domain == domain,
            StorageModel.username == username,
        )
        result = await self.session.execute(query)
        existing_storage = result.scalar_one_or_none()
        if existing_storage:
            existing_storage.storage_data = storage_data
            await self.session.flush()
            return existing_storage
        
        # 创建新记录
        new_storage = StorageModel(
            domain=domain,
            username=username,
            storage_data=storage_data,
        )
        self.session.add(new_storage)
        await self.session.flush()
        return new_storage

    async def get_storage(
        self,
        domain: str,
        username: str,
    ) -> Optional[StorageModel]:
        """获取指定域名和用户名的存储数据"""
        query = select(StorageModel).where(
            StorageModel.domain == domain,
            StorageModel.username == username
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() 