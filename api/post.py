from typing import Annotated, Optional
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Request
from controllers.post import (
    create_post,
    read_post,
    read_posts,
    update_post,
    delete_post,
)
from database import get_db
from schemas.post import PostCreate, PostUpdate
from helpers.auth import decode_jwt_token, verify_header
from schemas.user import Token

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)


@router.post("/")
def create_post_api(
    post: PostCreate,
    token: Annotated[str, Depends(verify_header)],
    db: Session = Depends(get_db),
):
    user = decode_jwt_token(token, db)
    response = create_post(db=db, token_user=user["username"], post=post)
    return {
        "message": "Post created successfully [ " + post.title + " ]",
        "contents": response,
    }


@router.get("/")
def read_posts_api(
    token: Annotated[str, Depends(verify_header)],
    db: Session = Depends(get_db),
):
    decode_jwt_token(token, db)
    response = read_posts(db=db)
    return {"message": "Posts retrieved successfully", "contents": response}


@router.get("/{id}")
def read_post_api(
    id: int,
    token: Annotated[str, Depends(verify_header)],
    db: Session = Depends(get_db),
):
    decode_jwt_token(token, db)
    response = read_post(id=id, db=db)
    return {
        "message": "Post read successfully with id " + str(id),
        "contents": response,
    }


# 게시글 수정
@router.put("/{id}")
def update_post_api(
    id: int,
    post: PostUpdate,
    token: Annotated[str, Depends(verify_header)],
    db: Session = Depends(get_db),
):
    user = decode_jwt_token(token, db)
    response = update_post(id=id, post=post, token_user=user["username"], db=db)
    return {
        "message": "Post updated successfully with id " + str(id),
        "contents": response,
    }


# 게시글 삭제
@router.delete("/{id}")
def delete_post_api(
    id: int,
    token: Annotated[str, Depends(verify_header)],
    db: Session = Depends(get_db),
):
    user = decode_jwt_token(token, db)
    delete_post(id=id, token_user=user["username"], db=db)
    return {"message": "Post deleted successfully"}
