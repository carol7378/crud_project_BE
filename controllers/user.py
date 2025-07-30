from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from datetime import timedelta
from helpers.auth import create_access_token
from constants.user import pwd_context
import schemas.user as schemas


def create_user(user: schemas.UserCreate, db: Session):
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="user_id already exists")
        db_user = User(username=user.username, password=user.password, name=user.name)
        db.add(db_user)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error [ " + e + " ]")


def login_user(user: schemas.UserLogin, db: Session):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        access_token = create_access_token(
            data=schemas.TokenEncode(username=db_user.username, id=db_user.id)
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error [ " + e + " ]")
