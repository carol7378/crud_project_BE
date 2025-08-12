from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
import datetime
from models.user import User as DB_User
from models.post import Post as DB_Post
from schemas.post import PostCreate, PostUpdate


# 게시글 작성
def create_post(post: PostCreate, user: DB_User, db: Session):
    db_post = DB_Post(
        title=post.title,
        user_id=user.id,
        content=post.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    response = {
        "message": "새로운 게시글이 등록되었습니다!",
        "id": db_post.id,
        "title": db_post.title,
        "username": user.username,
    }
    return response


# 게시글 10개씩 불러오기
def read_posts(page: int, db: Session):
    if page < 0:
        raise HTTPException(status_code=400, detail="wrong page number")
    total = db.query(DB_Post).filter(DB_Post.removed_at.is_(None)).count()
    posts_query = (
        select(DB_Post.id, DB_Post.title, DB_User.username, DB_Post.create_at)
        .join(DB_User, DB_User.id == DB_Post.user_id)
        .filter(DB_Post.removed_at.is_(None))
        .order_by(DB_Post.create_at.desc())
        .offset(page * 10)
        .limit(10)
    )
    posts = db.execute(posts_query).all()
    return {
        "total": total,
        "page": page + 1,
        "limit": 10,
        "page_data": posts,
    }


# 게시글 1건 조회
def read_post(id: int, db: Session):
    db_post = db.execute(
        select(
            DB_Post.id,
            DB_Post.title,
            DB_Post.content,
            DB_Post.create_at,
            DB_User.username,
        )
        .filter(DB_Post.id == id, DB_Post.removed_at.is_(None))
        .join(DB_Post, DB_Post.user_id == DB_User.id)
    ).first()
    return db_post


# 게시글 수정
def update_post(id: int, post: PostUpdate, user: DB_User, db: Session):
    db_post = (
        db.query(DB_Post).filter(DB_Post.id == id, DB_Post.removed_at.is_(None)).first()
    )
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=401, detail="username not match")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    return {"success": True}


# 게시글 삭제
def delete_post(id: int, user: DB_User, db: Session):
    db_post = (
        db.query(DB_Post).filter(DB_Post.id == id, DB_Post.removed_at.is_(None)).first()
    )
    if db_post is None:
        raise HTTPException(status_code=400, detail="wrong post id")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=401, detail="username not match")
    db_post.removed_at = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    db.commit()
    return {"success": True}
