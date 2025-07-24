from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator,model_validator

class Token(BaseModel):
    access_token:str
    token_type:str
    user_id:str

class UserCreate(BaseModel):
    username: str 
    password: str
    password_check: str 
    name: str 

    @field_validator('username', 'password', 'name', 'password_check')
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail='빈 값은 허용되지 않습니다.')
#            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @model_validator(mode='after')
    @classmethod
    def passwords_match(cls,values):
        if values.password!=values.password_check:
            raise HTTPException(status_code=400, detail='비밀번호가 일치하지 않습니다')
#            raise ValueError('비밀번호가 일치하지 않습니다')
        return values