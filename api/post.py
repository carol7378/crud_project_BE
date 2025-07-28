from typing import Annotated
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from controllers.post import (
    create_post,
    read_post,
    read_posts,
    update_post,
    delete_post,
)
from database import get_db
from schemas.post import PostCreate, PostUpdate
from helpers.auth import decode_jwt_token
from schemas.user import Token

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)
api_key_header = APIKeyHeader(name="Token")


@router.post("/")
def post_create(
    post: PostCreate,
    Token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    payload = decode_jwt_token(Token)
    response = create_post(db=db, token_user=payload["username"], post=post)
    return {
        "message": "Post created successfully [ " + post_create.title + " ]",
        "contents": response,
    }


@router.get("/")
def posts_read(
    Token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    decode_jwt_token(Token)
    response = read_posts(db=db)
    return {"message": "Posts retrieved successfully", "contents": response}


@router.get("/{id}")
def post_read(
    id: int,
    Token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    payload = decode_jwt_token(Token)
    response = read_post(id=id, db=db)
    return {
        "message": "Post read successfully with id " + str(id),
        "contents": response,
    }


# 게시글 수정
@router.put("/{id}")
def post_update(
    id: int,
    post: PostUpdate,
    Token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    payload = decode_jwt_token(Token)
    response = update_post(id=id, post=post, token_user=payload["username"], db=db)
    return {
        "message": "Post updated successfully with id " + str(id),
        "contents": response,
    }


# 게시글 삭제
@router.delete("/{id}")
def post_delete(
    id: int,
    Token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    payload = decode_jwt_token(Token)
    delete_post(id=id, token_user=payload["username"], db=db)
    return {"message": "Post deleted successfully"}
