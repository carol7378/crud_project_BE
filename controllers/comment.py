from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from models.comment import Comment as DB_Comment
from models.user import User as DB_User
from schemas.comment import CommentCreate, CommentUpdate
import datetime
import pytz


# 댓글 작성
def create_comment(
    post_id: int, user: DB_User, comment: CommentCreate, db: Session
):
    db_comment = DB_Comment(
        post_id=post_id, user_id=user.id, content=comment.content
    )
    db.add(db_comment)
    db.commit()
    return {"message": "댓글 작성이 완료되었습니다.", "id": db_comment.id}


# 댓글 10개씩 조회
def read_comments(post_id: int, page: int, db: Session):
    if page < 0:
        raise HTTPException(status_code=400, detail="wrong page number")
    total = (
        db.query(DB_Comment)
        .filter(DB_Comment.post_id == post_id, DB_Comment.removed_at.is_(None))
        .count()
    )
    comments_query = (
        select(
            DB_Comment.id,
            DB_Comment.content,
            DB_Comment.created_at,
            DB_User.username,
        )
        .join(DB_User, DB_User.id == DB_Comment.user_id)
        .filter(DB_Comment.post_id == post_id, DB_Comment.removed_at.is_(None))
        .order_by(DB_Comment.id.asc())
        .offset(page * 10)
        .limit(10)
    )
    comments = db.execute(comments_query).all()
    return {
        "total": total,
        "page": page + 1,
        "limit": 10,
        "comments": comments,
    }


# 댓글 수정
def update_comment(id: int, user: DB_User, comment: CommentUpdate, db: Session):
    db_comment = (
        db.query(DB_Comment)
        .filter(DB_Comment.id == id, DB_Comment.removed_at.is_(None))
        .first()
    )
    if db_comment is None:
        raise HTTPException(status_code=400, detail="wrong comment id")
    if db_comment.user_id != user.id:
        raise HTTPException(status_code=401, detail="username not match")
    db_comment.content = comment.content
    db.commit()
    return {"success": True}


# 댓글 삭제
def delete_comment(id: int, user: DB_User, db: Session):
    db_comment = (
        db.query(DB_Comment)
        .filter(DB_Comment.id == id, DB_Comment.removed_at.is_(None))
        .first()
    )
    if db_comment is None:
        raise HTTPException(status_code=400, detail="wrong comment id")
    if db_comment.user_id != user.id:
        raise HTTPException(status_code=401, detail="username not match")
    db_comment.removed_at = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    db.commit()
    return {"success": True, "id": db_comment.id}
