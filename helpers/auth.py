from constants.user import ACCESS_TOKEN_EXPIRE_MINUTES
import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import jwt
import pytz
from database import get_db
from models.user import User
from schemas.user import TokenEncode

SECRET_KEY = "a840e971b790eb005b7f6a1be72fb977d687f7d5d28be909ab4db9239174eef8"
ALGORITHM = "HS256"

auth_header = APIKeyHeader(name="Authorization", auto_error=False)


def create_access_token(
    data: TokenEncode,
    expires_delta: Optional[datetime.timedelta] = datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ),
):
    encode_data = {
        "username": data.username,
        "id": data.id,
        "exp": datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        + expires_delta,
    }
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(
    Authorization: str = Depends(auth_header), db: Session = Depends(get_db)
):
    try:
        if Authorization is None:
            raise HTTPException(status_code=401, detail="Authorization Error")
        if (
            len(Authorization.split()) != 2
            or Authorization.split()[0] != "Bearer"
        ):
            raise HTTPException(status_code=401, detail="Authorization Error")
        token = Authorization.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=400, detail="잘못된 토큰입니다.")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=400, detail="사용자를 찾을 수 없습니다"
            )
        return user
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")

    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="옳지 않은 토큰입니다.")
