from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from controllers.comment import (
    create_comment,
    read_comments,
    update_comment,
    delete_comment,
)
from database import get_db
from models.user import User
from schemas.comment import CommentCreate, CommentUpdate, CommentPagination
from helpers.auth import decode_jwt_token

router = APIRouter(prefix="/api", tags=["Comments"])

tokenDep = Annotated[User, Depends(decode_jwt_token)]
dbDep = Annotated[Session, Depends(get_db)]


# 댓글 작성
@router.post("/posts/{post_id}/comments")
def create_comment_api(
    post_id: int, comment: CommentCreate, user: tokenDep, db: dbDep
):
    response = create_comment(
        post_id=post_id, comment=comment, user=user, db=db
    )
    return {"success": True, "comment_id": response["id"]}


# 댓글 목록 조회
@router.get("/posts/{post_id}/comments", response_model=CommentPagination)
def read_comments_api(
    post_id: int,
    user: tokenDep,
    db: dbDep,
    page: int = Query(1),
):
    response = read_comments(post_id=post_id, db=db, page=page - 1)
    return response


# 댓글 수정
@router.put("/comments/{id}")
def update_comment_api(
    id: int, comment: CommentUpdate, user: tokenDep, db: dbDep
):
    return update_comment(id=id, user=user, comment=comment, db=db)


# 댓글 삭제
@router.delete("/comments/{id}")
def delete_comment_api(id: int, user: tokenDep, db: dbDep):
    return delete_comment(id=id, user=user, db=db)
