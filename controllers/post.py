import pytz
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
import datetime
from models.user import User as DB_User
from models.post import Post as DB_Post
from schemas.post import PostBase, PostCreate, Post, PostUpdate


# 게시글 작성
def create_post(post: PostCreate, token_user: str, db: Session):
    existing_user = db.query(DB_User).filter(DB_User.username == post.username).first()
    if token_user != existing_user.username:
        # 권한 없음
        raise HTTPException(status_code=401, detail="username not match")
    db_post = DB_Post(
        title=post.title,
        user_id=existing_user.id,
        content=post.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"success": True}


# 게시글 1건 조회
def read_post(id: int, db: Session):
    db_post = db.query(DB_Post).filter(DB_Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(
        id=db_post.id,
        title=db_post.title,
        username=db_post.user.username,
        content=db_post.content,
        create_at=db_post.create_at,
    )


# 게시글 리스트 조회
def read_posts(db: Session):
    posts = db.query(DB_Post).filter(DB_Post.removed_at == None).all()
    all_post = [
        PostBase(
            id=post.id,
            title=post.title,
            username=post.user.username,
            create_at=post.create_at,
        )
        for post in posts
    ]
    all_post = sorted(all_post, key=lambda post: post.create_at)
    all_post.reverse()
    return all_post


# 게시글 수정
def update_post(id: int, post: PostUpdate, token_user: str, db: Session):
    db_post = (
        db.query(DB_Post).filter(DB_Post.id == id, DB_Post.removed_at == None).first()
    )
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")
    if token_user != db_post.user.username:
        # 권한 없음
        raise HTTPException(status_code=401, detail="username not match")
    db_post.title = post.title
    db_post.content = post.content
    db_post.create_at = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    db.commit()
    db.refresh(db_post)
    return Post(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        username=db_post.user.username,
        create_at=db_post.create_at,
    )


# 게시글 삭제
def delete_post(id: int, token_user: str, db: Session):
    db_post = (
        db.query(DB_Post).filter(DB_Post.id == id, DB_Post.removed_at == None).first()
    )
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")

    db_user = db.query(DB_User).filter(DB_User.id == db_post.user_id).first()
    if token_user != db_user.username:
        raise HTTPException(status_code=401, detail="username not match")
    db_post.removed_at = datetime.datetime.now()
    db.commit()
    db.refresh(db_post)
    return
