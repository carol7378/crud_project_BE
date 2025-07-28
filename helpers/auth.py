import datetime
from typing import Optional
import jwt

from schemas.user import TokenEncode

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"


def create_access_token(
    data: TokenEncode,
    expires_delta: Optional[datetime.timedelta] = datetime.timedelta(seconds=15),
):
    encode_data = TokenEncode(
        username=data.username,
        id=data.id,
        exp=datetime.datetime.now() + expires_delta,
    )
    encoded_jwt = jwt.encode(encode_data.__dict__, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
