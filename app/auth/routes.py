from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.oauth2 import create_token
from app.auth.schemas import TokenOut, UserIn, UserOut
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
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    if not verify_pwd(user_details.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    token = create_token(data={"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


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
