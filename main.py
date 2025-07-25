from fastapi import FastAPI
import models.user as User
#import models.post as Post
import database
#from api import post
from api import user

app = FastAPI()

User.Base.metadata.create_all(bind=database.engine)
#Post.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user.router)
#app.include_router(post.router)