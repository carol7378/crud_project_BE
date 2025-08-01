from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        {"mysql_character_set": "utf8mb4", "mysql_collate": "utf8mb4_0900_as_cs"},
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="각 게시물을 구별하기 위한 ID",
    )
    title: Mapped[str] = mapped_column(String(100), comment="게시물 제목")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="게시물 작성자",
    )
    content: Mapped[str] = mapped_column(String(300), comment="게시물 내용")
    create_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        comment="게시물이 업로드된 시각",
    )
    removed_at: Mapped[datetime | None] = mapped_column(
        comment="게시물이 삭제된 시각 (삭제되지 않은 게시물은 Null)",
    )
