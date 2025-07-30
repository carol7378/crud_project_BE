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
from models.user import User
from schemas.post import PostCreate, PostUpdate
from helpers.auth import decode_jwt_token
from schemas.user import Token

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.post("/")
def create_post_api(
    post: PostCreate,
    user: Annotated[User, Depends(decode_jwt_token)],
    db: Annotated[Session, Depends(get_db)],
):
    response = create_post(db=db, user=user, post=post)
    return response


@router.get("/")
def read_posts_api(
    user: Annotated[User, Depends(decode_jwt_token)],
    db: Session = Depends(get_db),
):
    response = read_posts(db=db)
    return response


@router.get("/{id}")
def read_post_api(
    id: int,
    user: Annotated[User, Depends(decode_jwt_token)],
    db: Session = Depends(get_db),
):
    response = read_post(id=id, db=db)
    return response


# 게시글 수정
@router.put("/{id}")
def update_post_api(
    id: int,
    post: PostUpdate,
    user: Annotated[User, Depends(decode_jwt_token)],
    db: Session = Depends(get_db),
):
    response = update_post(id=id, post=post, user=user, db=db)
    return response


# 게시글 삭제
@router.delete("/{id}")
def delete_post_api(
    id: int,
    user: Annotated[User, Depends(decode_jwt_token)],
    db: Session = Depends(get_db),
):
    response = delete_post(id=id, user=user, db=db)
    return response
