from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from chrome_auto_server.db.base import Base

class CookieModel(Base):
    """Cookie存储模型"""
    
    __tablename__ = "cookies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String, nullable=False, comment="域名")
    username = Column(String, nullable=False, comment="用户名")
    cookie_data = Column(JSON, nullable=False, comment="Cookie数据")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        # 创建domain和username的联合唯一索引
        {'mysql_charset': 'utf8mb4'}
    ) 