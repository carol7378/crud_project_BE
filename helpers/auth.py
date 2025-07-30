import datetime
from typing import Optional
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt
import pytz
from models.user import User
from schemas.user import TokenEncode

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
from constants.user import ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(
    data: TokenEncode,
    expires_delta: Optional[datetime.timedelta] = datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ),
):
    encode_data = {
        "username": data.username,
        "id": data.id,
        "exp": datetime.datetime.now(pytz.timezone("Asia/Seoul")) + expires_delta,
    }
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=400, detail="잘못된 토큰입니다.")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=400, detail="사용자를 찾을 수 없습니다")
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="옳지 않은 토큰입니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error [ " + e + " ]")


def verify_header(Authorization: Optional[str] = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization Error")
    return Authorization
