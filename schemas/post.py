
import datetime
from pydantic import BaseModel, Field

class Post(BaseModel):
    id : int
    title: str 
    username: str
    content: str 
    create_at: datetime.datetime

class PostUpdate(BaseModel):
    token: str
    title: str 
    content: str 

class PostCreate(BaseModel):
    title: str = Field(..., max_length=100)
    username: str
    content: str = Field(..., max_length=300)

    class Config:
        from_attributes = True