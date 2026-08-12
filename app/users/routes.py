from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.users.models import Users
from app.users.schemas import UserProfile

router = APIRouter()


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserProfile)
async def fetch_profile(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = db.query(Users).filter(Users.id == current_user.id).first()
    return fetched
