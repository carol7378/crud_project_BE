from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


# 게시글 전체 조회 출력 형식
class PostBase(BaseModel):
    id: int = Field(..., description="게시글에 대한 id")
    title: str = Field(..., description="게시글 제목")
    username: str = Field(..., description="작성자의 닉네임")
    create_at: str = Field(..., description="게시글 생성시간")

    @field_validator("create_at", mode="before")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%Y-%m-%d %H:%M:%S")


class PostPagination(BaseModel):
    total: int = Field(..., description="게시글 전체 개수")
    page: int = Field(..., description="현재 페이지")
    limit: int = Field(..., description="페이지 당 게시글 수")
    page_data: list[PostBase] = Field(..., description="가져온 10개의 게시글 데이터")


# 게시글 상세 조회 출력 형식
class PostDetail(PostBase):
    content: str = Field(..., description="게시글 본문")


# 게시글 만들 때 입력 형식
class PostCreate(BaseModel):
    title: str = Field(..., description="게시글 제목", max_length=100)
    content: str = Field(..., description="게시글 본문", max_length=300)

    @field_validator("title", "content", mode="before")
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v


# 게시글 수정할 때 입력 형식
class PostUpdate(PostCreate):
    pass
