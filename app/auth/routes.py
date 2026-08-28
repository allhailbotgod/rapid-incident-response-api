from datetime import datetime, timezone

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.models import RevokedTokens
from app.auth.oauth2 import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
)
from app.auth.schemas import RefreshTokenRequest, TokenOut, UserIn, UserOut
from app.database import get_db
from app.roles.models import Roles
from app.users.models import Users
from app.utils.pwd import hash_pwd, verify_pwd

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenOut)
def user_login(
    user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(Users).filter(user_details.username == Users.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )

    if not verify_pwd(user_details.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )

    access_token = create_access_token(data={"sub": str(user.id), "type": "access"})

    refresh_token, refresh_token_jti = create_refresh_token(
        data={"sub": str(user.id), "type": "refresh"}
    )

    new_revoked_token = RevokedTokens(
        user_id=user.id, jti=refresh_token_jti, revoked=False
    )

    try:
        db.add(new_revoked_token)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Revoked token not added."
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured.",
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def user_registration(user: UserIn, db: Session = Depends(get_db)):
    default_role = db.query(Roles).filter(Roles.name == "regular").first()

    if default_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Default role not found."
        )

    new_user = Users(
        **user.model_dump(exclude={"password"}),
        role_id=default_role.id,
        password=hash_pwd(user.password)
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists."
        )

    return new_user


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenOut)
def user_token_refresh_request(
    token: RefreshTokenRequest, db: Session = Depends(get_db)
):
    payload = verify_refresh_token(token=token.refresh_token, db=db)

    set_revoked = (
        db.query(RevokedTokens)
        .join(Users)
        .filter(RevokedTokens.jti == payload["jti"], Users.id == payload["sub"])
        .first()
    )

    if set_revoked is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cannot generate new tokens."
        )

    set_revoked.revoked = True
    set_revoked.revoked_at = datetime.now(timezone.utc)

    new_access_token = create_access_token(data={"sub": payload["sub"]})

    new_refresh_token, refresh_token_jti = create_refresh_token(
        data={"sub": payload["sub"]}
    )

    new_revoked_token = RevokedTokens(
        user_id=payload["sub"], jti=refresh_token_jti, revoked=False
    )

    try:
        db.add(new_revoked_token)
        db.commit()
        db.refresh(set_revoked)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Revoked token not added."
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured.",
        )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
