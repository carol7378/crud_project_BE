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
        raise HTTPException(status_code=400, detail="username not match")
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
    db_post = db.execute(
        select(DB_Post, DB_User).join(DB_User, DB_User.id == DB_Post.user_id)
    ).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # db_username = (
    #     db.query(DB_User).filter(DB_User.id == db_post.user_id).first().username
    # )
    return Post(
        id=db_post.id,
        title=db_post.title,
        username=db_post.username,
        content=db_post.content,
        create_at=db_post.create_at,
    )


# 게시글 리스트 조회
def read_posts(db: Session):
    db_post = db.query(DB_Post).filter(DB_Post.removed_at == None).all()
    all_post = []

    for posts in db_post:
        db_username = (
            db.query(DB_User).filter(DB_User.id == posts.user_id).first().username
        )
        all_post.append(
            PostBase(
                id=posts.id,
                title=posts.title,
                username=db_username,
                create_at=posts.create_at,
            )
        )
    all_post = sorted(all_post, key=lambda post: post.create_at)
    all_post.reverse()
    return all_post


# 게시글 수정
def update_post(id: int, post: PostUpdate, token_user: str, db: Session):
    db_post = db.query(DB_Post).filter(DB_Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")
    db_user = db.query(DB_User).filter(DB_User.id == db_post.user_id).first()
    if token_user != db_user.username:
        raise HTTPException(status_code=400, detail="username not match")
    if db_post.removed_at is not None:
        raise HTTPException(status_code=404, detail="Post has been removed")
    db_post.title = post.title
    db_post.content = post.content
    db_post.create_at = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    db.commit()
    db.refresh(db_post)
    return Post(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        username=db_user,
        create_at=db_post.create_at,
    )


# 게시글 삭제
def delete_post(id: int, token_user: str, db: Session):
    db_post = db.query(DB_Post).filter(DB_Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="wrong post id")

    db_user = db.query(DB_User).filter(DB_User.id == db_post.user_id).first()
    if token_user != db_user.username:
        raise HTTPException(status_code=400, detail="username not match")
    if db_post.removed_at is not None:
        raise HTTPException(status_code=404, detail="already deleted post")
    db_post.removed_at = datetime.datetime.now()
    db.commit()
    db.refresh(db_post)
    return
