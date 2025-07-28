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
    id: int
    title: str
    username: str
    content: str
    create_at: datetime.datetime


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
