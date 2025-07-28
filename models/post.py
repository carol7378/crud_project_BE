from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import registry
from database import Base, engine

mapper_registry = registry()


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        {"mysql_character_set": "utf8mb4", "mysql_collate": "utf8mb4_0900_as_cs"},
    )
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="각 게시물을 구별하기 위한 ID",
    )
    title = Column(String(100), nullable=False, comment="게시물 제목")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시물 작성자",
    )
    content = Column(String(300), nullable=False, comment="게시물 내용")
    create_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="게시물이 업로드된 시각",
    )
    removed_at = Column(
        DateTime,
        nullable=True,
        comment="게시물이 삭제된 시각 (삭제되지 않은 게시물은 Null)",
    )
