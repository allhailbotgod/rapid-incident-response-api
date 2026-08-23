from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.agencies.models import Agency
from app.agencies.schemas import AgencyOut
from app.auth.oauth2 import get_current_user
from app.database import get_db

router = APIRouter()


@router.get("/agencies", status_code=status.HTTP_200_OK, response_model=AgencyOut)
def fetch_agencies(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = db.query(Agency).all()

    return fetched
