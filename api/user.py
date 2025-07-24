import os
import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
sys.path.insert(0, os.path.abspath('..'))
from schemas.user import UserCreate,UserLogin
from controllers.user import create_user, login_user
router = APIRouter(
    prefix="/api/users",
)

@router.post("/")
def user_create(user_create:UserCreate, db:Session=Depends(get_db)):
    create_user(db=db, user=user_create)
    return {"message": "User created successfully "+ user_create.username}

@router.post("/login")
def user_login(user_login:UserLogin, db:Session=Depends(get_db)):
    login_user(db=db, user=user_login)
    return {"message": "Welcome , "+ user_login.username+"!"}