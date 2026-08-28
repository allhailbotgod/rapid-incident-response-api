from uuid import uuid4

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.auth.models import RevokedTokens
from app.config import settings
from app.database import get_db
from app.users.models import Users

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRY = settings.ACCESS_TOKEN_EXPIRY_IN_MINS
REFRESH_TOKEN_EXPIRY = settings.REFRESH_TOKEN_EXPIRY_IN_DAYS


def create_access_token(data: dict):
    access_token_jti = str(uuid4())
    to_encode = data.copy()
    issued_at = datetime.now(timezone.utc)
    expiry = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRY)

    to_encode.update(
        {"jti": access_token_jti, "type": "access", "iat": issued_at, "exp": expiry}
    )

    encoded = jwt.encode(to_encode, algorithm=ALGORITHM, key=SECRET_KEY)

    return encoded


def create_refresh_token(data: dict):
    refresh_token_jti = str(uuid4())
    to_encode = data.copy()
    issued_at = datetime.now(timezone.utc)
    expiry = issued_at + timedelta(days=REFRESH_TOKEN_EXPIRY)

    to_encode.update(
        {"jti": refresh_token_jti, "type": "refresh", "iat": issued_at, "exp": expiry}
    )

    encoded = jwt.encode(to_encode, algorithm=ALGORITHM, key=SECRET_KEY)

    return encoded, refresh_token_jti


def verify_access_token(to_verify: str, credentials_exception):
    try:
        payload = jwt.decode(token=to_verify, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user_id


def verify_refresh_token(
    token: str,
    db: Session,
):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        jti: str = payload.get("jti")
        token_type = payload.get("type")

        if not user_id or not jti:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(Users).filter(Users.id == user_id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not exist.",
            )

        is_revoked = db.query(RevokedTokens).filter(RevokedTokens.jti == jti).first()

        if is_revoked is not None and is_revoked.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def get_current_user(
    fetched_token: str = Depends(OAuth2PasswordBearer(tokenUrl="/v1/auth/login")),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(
        to_verify=fetched_token, credentials_exception=credentials_exception
    )
    current_user = db.query(Users).filter(Users.id == user_id).first()

    return current_user
