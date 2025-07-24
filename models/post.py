from sqlalchemy import Boolean, Column , DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import registry
from database import Base,engine

mapper_registry = registry()

'''
# 컬럼 설명
    id = 각 게시물을 구별하기 위한 ID
    title = 게시물 제목
    username = 게시물 작성자
    content = 게시물 내용
    create_at = 게시물이 업로드된 시각
    removed_at = 게시물이 삭제된 시각 (삭제되지 않은 게시물은 Null)

'''
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(100), nullable=False)
    username = Column(String(30), ForeignKey('users.username',ondelete='CASCADE'),nullable=False)
    content = Column(String(300), nullable=False)
    create_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    removed_at = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)