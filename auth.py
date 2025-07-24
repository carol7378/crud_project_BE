import datetime
from typing import Optional
import jwt

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta]=datetime.timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.datetime.now(tz=datetime.UTC) +expires_delta
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt