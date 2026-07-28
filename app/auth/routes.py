from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.oauth2 import create_token
from app.auth.schemas import TokenOut, UserIn
from app.database import get_db
from app.roles.models import Roles
from app.users.models import Users
from app.utils.helpers import hash_pwd, verify_pwd

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenOut)
async def user_login(
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

    token = create_token(data={"user_id": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(user: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(user.email == Users.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email has already been used.",
        )

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
    db.commit()
    db.refresh(new_user)

    role = (
        db.query(Roles)
        .join(Users, Users.role_id == Roles.id)
        .filter(Users.id == new_user.id)
        .first()
    )

    return {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "phone": new_user.phone,
        "email": new_user.email,
        "gender": new_user.gender,
        "role": role.name,
    }
