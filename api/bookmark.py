from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from controllers.bookmark import read_bookmarks, add_bookmark, remove_bookmark
from database import get_db
from models.user import User
from schemas.bookmark import BookmarkResponse, BookmarkPagination
from helpers.auth import decode_jwt_token

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])

tokenDep = Annotated[User, Depends(decode_jwt_token)]
dbDep = Annotated[Session, Depends(get_db)]


# 북마크 게시글 목록 10개씩 조회
@router.get("/", response_model=BookmarkPagination)
def read_bookmarks_api(
    user: tokenDep,
    db: dbDep,
    page: int = Query(1),
):
    response = read_bookmarks(db=db, user_id=user.id, page=page - 1)
    return response


# 북마크 추가
@router.post("/{id}")
def create_bookmark(id: int, db: dbDep, user: tokenDep):
    response = add_bookmark(db, user.id, id)
    return response


# 북마크 삭제
@router.delete("/{id}")
def delete_bookmark(id: int, db: dbDep, user: tokenDep):
    return remove_bookmark(db, user.id, id)
