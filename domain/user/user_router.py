from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from .user_schema import UserCreate
from .user_crud import create_user

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create")
def user_create(user_create:UserCreate, db:Session=Depends(get_db)):
    create_user(db=db, user_create=user_create)
    return {"message": "User created successfully "+ user_create.username}