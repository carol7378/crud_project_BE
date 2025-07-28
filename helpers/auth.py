import datetime
from typing import Optional
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
