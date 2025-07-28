from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.user import User

# from models.post import Post
from datetime import timedelta
from helpers.auth import create_access_token
from constants.user import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context

import schemas.user as schemas
from datetime import timedelta
from helpers.auth import create_access_token
from constants.user import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context


def create_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user_id already exists")
    db_user = User(username=user.username, password=user.password, name=user.name)
    db.add(db_user)
    db.commit()


def login_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data=schemas.TokenEncode(username=db_user.username, id=db_user.id),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }
