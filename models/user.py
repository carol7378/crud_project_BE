from sqlalchemy import Boolean, Column , DateTime, ForeignKey, Integer, String
from database import Base,engine
from sqlalchemy.orm import registry
mapper_registry = registry()

'''
# 컬럼 설명
    id = 사용자에게 부여된 ID(int)
    username = 사용자 닉네임 (string, primary_key)
    name = 사용자 실제 이름
    password = 사용자 비밀번호

'''

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {'mysql_character_set': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_520_ci'},
    )
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(30) ,unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    
Base.metadata.create_all(engine)