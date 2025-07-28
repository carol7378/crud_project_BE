from fastapi import FastAPI
import models.user as User
import database
from api import user

app = FastAPI()

User.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
