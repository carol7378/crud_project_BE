from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import Token, UserCreate, UserLogin
from controllers.user import create_user, login_user

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

dbDep = Annotated[Session, Depends(get_db)]


@router.post("/")
def user_create(user_create: UserCreate, db: dbDep):
    create_user(db=db, user=user_create)
    return {"success": True}


@router.post("/login", response_model=Token)
def user_login(user_login: UserLogin, db: dbDep):
    response = login_user(db=db, user=user_login)
    return response
