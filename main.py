from fastapi import FastAPI
import models
import database
#from domain.post import post_router
from domain.user import user_router

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user_router.router)