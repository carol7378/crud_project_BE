
import datetime
from pydantic import BaseModel, Field

class Post(BaseModel):
    title: str 
    username: str
    content: str 

class PostUpdate(BaseModel):
    title: str 
    content: str 

class PostCreate(BaseModel):
    title: str = Field(..., max_length=100)
    username: str
    content: str = Field(..., max_length=300)

    class Config:
        from_attributes = True