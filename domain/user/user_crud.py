import models
import domain.user.user_schema as schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_create: schemas.UserCreate, db: Session):
    existing_user = db.query(models.User).filter(
        models.User.username == user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user_id already exists")
    db_user = models.User(status=True,username=user_create.username, password=pwd_context.hash(
        user_create.password), name=user_create.name)
    db.add(db_user)
    db.commit()