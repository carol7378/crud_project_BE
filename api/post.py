import json
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
import requests

router = APIRouter(prefix="/api/posts", tags=["Posts"])

tokenDep = Annotated[User, Depends(decode_jwt_token)]
dbDep = Annotated[Session, Depends(get_db)]


# 게시글 생성
@router.post("/")
def create_post_api(post: PostCreate_Update, user: tokenDep, db: dbDep):
    response = create_post(db=db, user=user, post=post)
    slackUrl = "https://hooks.slack.com/triggers/~"
    data = {
        "id": response[0],
        "title": response[1],
        "username": response[2],
        "content": response[3],
        "create_at": response[4].strftime("%Y-%m-%d %H:%M:%S"),
    }
    requests.post(slackUrl, data=json.dumps(data))
    return {"success": True, "post id": response[0]}


# 게시글 전체 조회
@router.get("/")
def read_posts_api(user: tokenDep, db: dbDep):
    response = read_posts(db=db)
    return response


# 게시글 1건 조회
@router.get("/{id}")
def read_post_api(id: int, user: tokenDep, db: dbDep):
    response = read_post(id=id, db=db)
    return response


# 게시글 수정
@router.put("/{id}")
def update_post_api(id: int, post: PostCreate_Update, user: tokenDep, db: dbDep):
    response = update_post(id=id, post=post, user=user, db=db)
    return response


# 게시글 삭제
@router.delete("/{id}")
def delete_post_api(id: int, user: tokenDep, db: dbDep):
    response = delete_post(id=id, user=user, db=db)
    return response
