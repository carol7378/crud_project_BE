from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import Token, UserCreate, UserLogin, PasswordUpdate
from controllers.user import create_user, login_user, update_password
from models.user import User
from helpers.auth import decode_jwt_token

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

dbDep = Annotated[Session, Depends(get_db)]
tokenDep = Annotated[User, Depends(decode_jwt_token)]


@router.post("/")
def user_create(user_create: UserCreate, db: dbDep):
    create_user(db=db, user=user_create)
    return {"success": True}


@router.post("/login", response_model=Token)
def user_login(user_login: UserLogin, db: dbDep):
    response = login_user(db=db, user=user_login)
    return response


@router.put("/password")
def password_update(password_update: PasswordUpdate, user: tokenDep, db: dbDep):
    response = update_password(data=password_update, user=tokenDep, db=db)
    return response
