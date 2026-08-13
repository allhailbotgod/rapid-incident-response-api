from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.sos.models import SOS
from app.sos.schemas import ContactIn, ContactOut, SOSResponse
from typing import List
from app.sos.models import SOS

router = APIRouter()


@router.post(
    "/contacts", status_code=status.HTTP_201_CREATED, response_model=ContactOut
)
def add_sos_contact(
    contact: ContactIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_contact = SOS(**contact.model_dump(), owner_id=current_user.id)

    db.add(new_contact)

    try:
        db.commit()
        db.refresh(new_contact)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This phone number is already an emergency contact.",
        )

    return new_contact


@router.get(
    "/contacts", status_code=status.HTTP_200_OK, response_model=List[SOSResponse]
)
def fetch_user_sos(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = db.query(SOS).filter(SOS.owner_id == current_user.id).all()
    return fetched
