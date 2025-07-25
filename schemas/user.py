import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from pydantic import BaseModel, Field, field_validator, model_validator


class TokenEncode(BaseModel):
    username: str
    id: int


class TokenEncode(BaseModel):
    username: str
    id: int
    exp: datetime.datetime = Field(default=datetime.datetime.now())


class Token(BaseModel):
    message: str
    access_token: str
    token_type: str
    username: str


class UserLogin(BaseModel):
    username: str
    password: str

    @model_validator(mode="before")
    @classmethod
    def not_empty(cls, values):
        for key, value in values.items():
            if value is None or str(value).strip() == "":
                raise HTTPException(
                    status_code=400, detail="빈 값은 허용되지 않습니다."
                )
        return values


class UserCreate(BaseModel):
    username: str = Field(..., description="사용자의 닉네임")
    password: str
    password_check: str = Field(..., description="작성한 비밀번호를 다시 입력")
    name: str = Field(..., description="사용자의 실제 이름")

    @field_validator("username", "password", "password_check", "name", mode="before")
    @classmethod
    def not_empty(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="빈 값은 허용되지 않습니다.")
        return v

    @model_validator(mode="after")
    @classmethod
    def passwords_match(cls, values):
        if values.password != values.password_check:
            raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다")
        return values
