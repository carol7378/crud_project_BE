from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from helpers.auth import create_access_token
from constants.user import pwd_context
import schemas.user as schemas


# 유저 생성
def create_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="user_id already exists")
    db_user = User(username=user.username, password=user.password, name=user.name)
    db.add(db_user)
    db.commit()


# 유저 로그인
def login_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data=schemas.TokenEncode(username=db_user.username, id=db_user.id)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


# 유저 비밀번호 변경
def update_password(id: int, data: schemas.PasswordUpdate, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user or not pwd_context.verify(data.current_password, db_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if data.new_password != data.new_password_check:
        raise HTTPException(
            status_code=400,
            detail="New password is incorrect"
        )
    db_user.password = pwd_context.hash(data.new_password)
    db.commit()
    return {"success": True}