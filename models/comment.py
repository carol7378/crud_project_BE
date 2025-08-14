from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from database import Base

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = (
        {"mysql_character_set": "utf8mb4", "mysql_collate": "utf8mb4_0900_as_cs"},
    )
    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        comment="댓글 id",
    )
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        comment="댓글 작성자 id",
    )
    post_id = Column(
        Integer, 
        ForeignKey("posts.id", ondelete="CASCADE"), 
        nullable=False,
        comment="댓글이 업로드된 게시글 id",
    )
    content = Column(
        String(300), 
        nullable=False, 
        comment="댓글 내용",
    )
    created_at = Column(
        DateTime, 
        server_default=text("CURRENT_TIMESTAMP"), 
        nullable=False,
        comment="댓글이 업로드된 시각",
    )
    removed_at = Column(
        DateTime, 
        nullable=True, 
        comment="댓글이 삭제된 시간",
    )
