from fastapi import HTTPException
from sqlalchemy.orm import Session
import schemas.user as schemas
from models.user import User
#from models.post import Post
from passlib.context import CryptContext
from datetime import timedelta
from auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(User).filter(
        User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user_id already exists")
    db_user = User(username=user.username, password=pwd_context.hash(
        user.password), name=user.name)
    db.add(db_user)
    db.commit()

def login_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(User).filter(User.username==user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not pwd_context.verify(user.password,db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub":db_user.name},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token":access_token,"token_type":"bearer"}
