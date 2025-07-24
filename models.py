from sqlalchemy import Boolean, Column , DateTime, ForeignKey, Integer, String
from database import Base,engine
from sqlalchemy.orm import registry
mapper_registry = registry()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    status = Column(Boolean, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(100), nullable=False)
    username = Column(String(30), ForeignKey('users.username',ondelete='CASCADE'),nullable=False)
    content = Column(String(300), nullable=False)
    create_at = Column(DateTime, nullable=False)
    removed_at = Column(DateTime, nullable=True)

print(Base.metadata.create_all(engine))
