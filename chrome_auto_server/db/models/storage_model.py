from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, DateTime, JSON

from chrome_auto_server.db.base import Base


class StorageModel(Base):
    """Model for storing browser storage data."""

    __tablename__ = "storage"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(length=255))  # 域名
    username: Mapped[str] = mapped_column(String(length=100))  # 用户名
    storage_data: Mapped[dict] = mapped_column(JSON)  # 存储数据（localStorage等）
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )  # 创建时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )  # 更新时间 