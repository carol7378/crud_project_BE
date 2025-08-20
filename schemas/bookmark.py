from pydantic import BaseModel, Field, field_validator


# 북마크 조회 형식
class BookmarkBase(BaseModel):
    id: int = Field(..., description="북마크 id")
    post_id: int = Field(..., description="북마크한 게시글 id")
    title: str = Field(..., description="게시글 제목")
    username: str = Field(..., description="게시글 작성자 닉네임")
    create_at: str = Field(..., description="게시글 생성시간")

    @field_validator("create_at", mode="before")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%Y-%m-%d %H:%M:%S")


class BookmarkPagination(BaseModel):
    total: int = Field(..., description="북마크 전체 개수")
    page: int = Field(..., description="현재 페이지")
    limit: int = Field(..., description="페이지 당 북마크 수")
    bookmarks: list[BookmarkBase] = Field(..., description="북마크 목록 데이터")


# 북마크 추가/삭제
class BookmarkResponse(BaseModel):
    id: int = Field(..., description="북마크 id")
    user_id: int = Field(..., description="북마크 하는 사용자 id")
    post_id: int = Field(..., description="북마크한 게시글 id")
