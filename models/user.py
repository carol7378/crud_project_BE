from sqlalchemy import VARBINARY, Column, Integer, String, BINARY
from constants.user import pwd_context
from database import Base, engine
from sqlalchemy.orm import registry

mapper_registry = registry()


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"mysql_character_set": "utf8mb4", "mysql_collate": "utf8mb4_0900_as_cs"},
    )
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="사용자에게 부여된 ID(int)",
    )
    username = Column(
        String(30),
        unique=True,
        nullable=False,
        comment="사용자 닉네임 (string, primary_key)",
    )
    name = Column(String(30), nullable=False, comment="사용자 실제 이름")
    password = Column(String(100), nullable=False, comment="사용자 비밀번호")

    def __init__(self, username: VARBINARY, name: str, password: str):
        self.username = username
        self.name = name
        self.password = pwd_context.hash(password)


Base.metadata.create_all(engine)
