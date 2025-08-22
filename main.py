from fastapi import FastAPI
from database import Base, engine
from api import user, post, comment, bookmark
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 프론트엔드 연결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(bookmark.router)
Base.metadata.create_all(bind=engine)
