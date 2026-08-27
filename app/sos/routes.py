from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from uuid import UUID
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.sos.models import SOS
from app.sos.schemas import ContactIn, ContactOut, SOSPatch, SOSResponse
from typing import List
from app.sos.models import SOS
from app.users.models import Users

router = APIRouter()


@router.post(
    "/contacts", status_code=status.HTTP_201_CREATED, response_model=ContactOut
)
def add_sos_contact(
    contact: ContactIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
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
    db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)
):
    fetched = db.query(SOS).filter(SOS.owner_id == current_user.id).all()
    return fetched


@router.patch(
    "/contacts/{id}", status_code=status.HTTP_200_OK, response_model=SOSResponse
)
def update_contact_info(
    id: UUID,
    update_contact: SOSPatch,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    to_update = (
        db.query(SOS).filter(SOS.id == id, SOS.owner_id == current_user.id).first()
    )

    if not to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found."
        )

    updates = update_contact.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in updates.items():
        setattr(to_update, key, value)

    to_update.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(to_update)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This phone number is already an emergency contact.",
        )

    return to_update


@router.delete("/contacts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contacts(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    to_delete = (
        db.query(SOS).filter(SOS.id == id, SOS.owner_id == current_user.id).first()
    )

    if to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found."
        )

    db.delete(to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
