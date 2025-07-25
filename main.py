from fastapi import FastAPI
import models.user as User
import database
from api import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

User.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
