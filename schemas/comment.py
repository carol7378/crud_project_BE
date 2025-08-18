from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

class CommentBase(BaseModel):
    id: int = Field(..., description="댓글에 대한 id")
    username: str = Field(..., description="작성자의 닉네임")
    content: str = Field(..., description="댓글 내용")
    created_at: str = Field(..., description="댓글 생성시간")

    @field_validator("created_at", mode="before")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%Y-%m-%d %H:%M:%S")

class CommentPagination(BaseModel):
    total: int = Field(..., description="댓글 전체 개수")
    page: int = Field(..., description="현재 페이지")
    limit: int = Field(..., description="페이지 당 댓글 수")
    page_data: list[CommentBase] = Field(..., description="가져온 10개의 댓글 데이터")

class CommentCreate(BaseModel):
    content: str = Field(..., max_length=300)

    @field_validator("content", mode="before")
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v

class CommentUpdate(CommentCreate):
    pass
