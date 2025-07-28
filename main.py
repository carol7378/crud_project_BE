from fastapi import FastAPI
import models.post as Post
import models.user as User
import database
from api import user, post
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 프론트엔드 연결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

User.Base.metadata.create_all(bind=database.engine)
Post.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(post.router)
