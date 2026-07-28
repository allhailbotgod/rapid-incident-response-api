from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.oauth2 import create_token
from app.auth.schemas import TokenOut
from app.database import get_db
from app.users.models import Users
from app.utils.helpers import verify_pwd

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

    token = create_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}
