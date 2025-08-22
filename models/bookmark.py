from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post"),
        {
            "mysql_character_set": "utf8mb4",
            "mysql_collate": "utf8mb4_0900_as_cs",
        },
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="북마크 id"
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="사용자 id"
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        comment="북마크한 게시글 id"
    )
