import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import pytz
from schemas.user import TokenEncode

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"


def create_access_token(
    data: TokenEncode,
    expires_delta: Optional[datetime.timedelta] = datetime.timedelta(minutes=30),
):
    encode_data = {
        "username": data.username,
        "id": data.id,
        "exp": datetime.datetime.now(pytz.timezone("Asia/Seoul")) + expires_delta,
    }
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=400, detail="잘못된 토큰입니다.")
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=400, detail="토큰이 만료되었습니다.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail="옳지 않은 토큰입니다.")
