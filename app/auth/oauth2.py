from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings
from app.database import get_db
from app.users.models import Users

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRY_IN_MINUTES = settings.EXP_IN_MINS


def create_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_IN_MINUTES)
    issued_at = datetime.now(timezone.utc)
    to_encode.update({"exp": expiry, "iat": issued_at})

    encoded = jwt.encode(to_encode, algorithm=ALGORITHM, key=SECRET_KEY)

    return encoded


def verify_token(to_verify: str, credentials_exception):
    try:
        payload = jwt.decode(token=to_verify, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user_id


def get_current_user(
    fetched_token: str = Depends(OAuth2PasswordBearer(tokenUrl="/v1/auth/login")),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_token(
        to_verify=fetched_token, credentials_exception=credentials_exception
    )
    current_user = db.query(Users).filter(Users.id == user_id).first()

    return current_user
