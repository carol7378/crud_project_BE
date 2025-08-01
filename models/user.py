from constants.user import pwd_context
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        {"mysql_character_set": "utf8mb4", "mysql_collate": "utf8mb4_0900_as_cs"},
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="사용자에게 부여된 ID(int)",
    )
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        comment="사용자 아이디 (string, primary_key)",
    )
    name: Mapped[str] = mapped_column(String(30), comment="사용자 실제 이름")
    password: Mapped[str] = mapped_column(String(100), comment="사용자 비밀번호")

    def __init__(self, username: str, name: str, password: str):
        self.username = username
        self.name = name
        self.password = pwd_context.hash(password)
