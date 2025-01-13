from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DanmakuCreate(BaseModel):
    """用于创建弹幕的模型."""
    content: str
    author: str


class DanmakuModel(BaseModel):
    """弹幕返回模型."""
    id: int
    content: str
    author: str
    created_at: datetime

    class Config:
        """配置."""
        from_attributes = True 

class DanmakuResponse(BaseModel):
    success: bool
    message: str
    data: Optional[DanmakuModel] = None 