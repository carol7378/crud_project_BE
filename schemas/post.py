import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
import pytz


class PostBase(BaseModel):
    id: int
    title: str
    username: str
    create_at: datetime.datetime


class Post(BaseModel):
    id: int = Field(..., description="게시글에 대한 id")
    title: str = Field(..., description="게시글 제목")
    username: str = Field(..., description="작성자의 닉네임")
    content: str = Field(..., description="게시글 본문")
    create_at: datetime.datetime = Field(..., description="게시글 생성시간")


class PostUpdate(BaseModel):
    title: str
    content: str

    @field_validator("title", "content", mode="before")
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v


class PostCreate(BaseModel):
    title: str = Field(..., max_length=100)
    username: str
    content: str = Field(..., max_length=300)

    @field_validator("username", "title", "content", mode="before")
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v

    class Config:
        from_attributes = True
