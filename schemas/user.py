import re
from fastapi import HTTPException
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)

from pydantic import BaseModel, Field, field_validator, model_validator


# 유저 로그인 시 토큰 생성 형식
class TokenEncode(BaseModel):
    username: str = Field(..., description="토큰 내 username")
    id: int = Field(..., description="토큰 내 user 의 id")


# 유저 로그인에 대한 토큰 내용 출력 형식
class Token(BaseModel):
    access_token: str = Field(..., description="토큰")
    token_type: str = Field(..., description="Bearer")
    username: str = Field(..., description="토큰이 할당된 유저의 username")


# 유저 생성 시 입력 형식
class UserCreate(BaseModel):
    username: str = Field(..., description="사용자의 닉네임")
    password: str = Field(..., description="사용자 비밀번호")
    password_check: str = Field(..., description="작성한 비밀번호를 다시 입력")
    name: str = Field(..., description="사용자의 실제 이름")

    @field_validator("password", mode="before")
    @classmethod
    def password_form(cls, v):
        if not re.compile(r"^[A-Za-z\d]{8,16}$").match(v):
            raise HTTPException(
                status_code=400,
                detail="비밀번호는 최소 8자, 촤대 16자이며, 알파벳과 숫자로 구성됩니다.",
            )
        return v

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


# 유저 로그인 시 입력 형식
class UserLogin(BaseModel):
    username: str = Field(..., description="사용자의 닉네임")
    password: str = Field(..., description="사용자의 비밀번호")

    @model_validator(mode="before")
    @classmethod
    def not_empty(cls, values):
        for key, value in values.items():
            if value is None or str(value).strip() == "":
                raise HTTPException(
                    status_code=400, detail="빈 값은 허용되지 않습니다."
                )
        return values
