from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import Token, UserCreate, UserLogin
from controllers.user import create_user, login_user

router = APIRouter(
    prefix="/api/users",
)


@router.post("/")
def user_create(user_create: UserCreate, db: Session = Depends(get_db)):
    create_user(db=db, user=user_create)
    return {"message": "User created successfully " + user_create.username}


@router.post("/login", response_model=Token)
def user_login(user_login: UserLogin, db: Session = Depends(get_db)):
    response = login_user(db=db, user=user_login)
    response["message"] = "Welcome , " + user_login.username + "!"
    return response
