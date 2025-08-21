from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.bookmark import Bookmark as DB_Bookmark
from models.post import Post as DB_Post
from models.user import User as DB_User


# 북마크 게시글 5개씩 불러오기
def read_bookmarks(db: Session, user_id: int, page: int):
    if page < 0:
        raise HTTPException(status_code=400, detail="wrong page number")
    total = (
        db.query(DB_Bookmark)
        .join(DB_Post, DB_Bookmark.post_id == DB_Post.id)
        .filter(
            DB_Bookmark.user_id == user_id,
            DB_Post.removed_at.is_(None)
        )
        .count()
    )
    bookmarks_query = (
        select(
            DB_Bookmark.id.label("id"),
            DB_Post.id.label("post_id"),
            DB_Post.title.label("title"),
            DB_User.username.label("username"),
            DB_Post.create_at.label("create_at")
        )
        .join(DB_Post, DB_Post.id == DB_Bookmark.post_id)
        .join(DB_User, DB_User.id == DB_Post.user_id)
        .filter(
            DB_Bookmark.user_id == user_id,
            DB_Post.removed_at.is_(None)
        )
        .order_by(DB_Bookmark.id.desc())
        .offset(page * 5)
        .limit(5)
    )
    bookmarks = db.execute(bookmarks_query).all()
    return {
        "total": total,
        "page": page + 1,
        "limit": 5,
        "bookmarks": bookmarks,
    }


# 북마크 추가
def add_bookmark(db: Session, user_id: int, post_id: int):
    post = db.query(DB_Post).filter(DB_Post.id == post_id,
                                    DB_Post.removed_at.is_(None)).first()
    if not post:
        raise HTTPException(status_code=400, detail="wrong post id")

    exists = db.query(DB_Bookmark).filter(
        DB_Bookmark.user_id == user_id,
        DB_Bookmark.post_id == post_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="already bookmarked")

    db_bookmark = DB_Bookmark(user_id=user_id, post_id=post_id)
    db.add(db_bookmark)
    db.commit()
    return {"success": True, "bookmark_id": db_bookmark.id}


# 북마크 삭제
def remove_bookmark(db: Session, user_id: int, post_id: int):
    bookmark = db.query(DB_Bookmark).filter(
        DB_Bookmark.user_id == user_id, DB_Bookmark.post_id == post_id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    db.delete(bookmark)
    db.commit()
    return {"success": True}
