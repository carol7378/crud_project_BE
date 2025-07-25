from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import datetime
from models.user import User
from models.post import Post
import schemas.post as post
from database import get_db

router = APIRouter(
    prefix="/api/posts",
)

#게시글 작성
def create_post(post: post.PostCreate, db: Session):
    existing_user = db.query(User).filter(
        User.username == post.username).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="username not found")
    db_post = Post(title=post.title, username=post.username,
                          content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 게시글 1건 조회
def read_post(id: int, db: Session):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if  db_post.removed_at is not None:
        raise HTTPException(status_code=404, detail="Post has been removed")
    return db_post

# 게시글 리스트 조회
def read_posts(db: Session):
    db_post = db.query(Post).filter(Post.removed_at == None).all()
    if not db_post:
        raise HTTPException(status_code=400, detail="Posts not found")
    return db_post

# 게시글 수정
def update_post(id: int, post: post.PostUpdate, db: Session):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")

    if  db_post.removed_at is not None:
        raise HTTPException(status_code=404, detail="Post has been removed")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.create_at = datetime.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post

# 게시글 삭제
def delete_post(id: int, db: Session):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="wrong post id")
    if db_post.removed_at is not None:
        raise HTTPException(status_code=404, detail="already deleted post")
    if db_post:
        db_post.removed_at = datetime.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post
