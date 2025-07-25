from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import datetime
from controllers.post import create_post, read_post, read_posts, update_post, delete_post
from database import get_db
from schemas.post import PostCreate, Post,PostUpdate

router = APIRouter(
    prefix="/api/posts",
)


@router.post("/")
def post_create(post_create:PostCreate, db:Session=Depends(get_db)):
    create_post(db=db, post= post_create)
    return {"message": "Post created successfully [ " + post_create.title+" ]"}

@router.get("/")
def posts_read(db: Session = Depends(get_db)):
    return {"message": "Posts retrieved successfully","contents":read_posts(db=db)}


@router.get("/{id}")
def post_read(id :int, db: Session = Depends(get_db)):
    return {"message": "Post read successfully with id " + str(id),"contents":read_post(id=id, db=db)}
    

# 게시글 수정
@router.put("/{id}")
def post_update(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    return {"message": "Post updated successfully with id " + str(id),"contents":update_post(id=id, post=post, db=db)}

#게시글 삭제
@router.delete("/{id}")
def post_delete(id: int, db: Session = Depends(get_db)):
    return {"message":"Post deleted successfully","contents":delete_post(id=id, db=db)}

