from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, DateTime

from chrome_auto_server.db.base import Base


class DanmakuModel(Base):
    """Model for storing danmaku (bullet comments) data."""

    __tablename__ = "danmaku"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(length=500))  # 弹幕内容
    author: Mapped[str] = mapped_column(String(length=100))   # 弹幕作者
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )  # 创建时间 