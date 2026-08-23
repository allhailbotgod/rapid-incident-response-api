from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.agencies.models import Agency
from app.agencies.schemas import AgencyIn, AgencyOut
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.utils.helpers import require_admin

router = APIRouter()


@router.get("/agencies", status_code=status.HTTP_200_OK, response_model=list[AgencyOut])
def fetch_agencies(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = db.query(Agency).all()

    return fetched


@router.post(
    "/agencies/register", status_code=status.HTTP_200_OK, response_model=AgencyOut
)
def register_agency(
    agency: AgencyIn,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    new_agency = Agency(**agency.model_dump())

    db.add(new_agency)

    try:
        db.commit()
        db.refresh(new_agency)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Agency already exists."
        )

    return new_agency
