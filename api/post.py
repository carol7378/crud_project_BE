from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from controllers.post import (
    create_post,
    read_post,
    read_posts,
    update_post,
    delete_post,
)
from database import get_db
from models.user import User
from schemas.post import PostCreate_Update
from helpers.auth import decode_jwt_token

router = APIRouter(prefix="/api/posts", tags=["Posts"])

token_user = Annotated[User, Depends(decode_jwt_token)]
db = Annotated[Session, Depends(get_db)]


# 게시글 생성
@router.post("/")
def create_post_api(post: PostCreate_Update, user: token_user, db: db):
    response = create_post(db=db, user=user, post=post)
    return response


# 게시글 전체 조회
@router.get("/")
def read_posts_api(user: token_user, db: db):
    response = read_posts(db=db)
    return response


# 게시글 1건 조회
@router.get("/{id}")
def read_post_api(id: int, user: token_user, db: db):
    response = read_post(id=id, db=db)
    return response


# 게시글 수정
@router.put("/{id}")
def update_post_api(id: int, post: PostCreate_Update, user: token_user, db: db):
    response = update_post(id=id, post=post, user=user, db=db)
    return response


# 게시글 삭제
@router.delete("/{id}")
def delete_post_api(id: int, user: token_user, db: db):
    response = delete_post(id=id, user=user, db=db)
    return response
