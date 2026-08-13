from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.medic.models import MedicProfile
from app.medic.schemas import MedicIn, MedicResponse

router = APIRouter()


@router.get("/medicals", status_code=status.HTTP_200_OK, response_model=MedicResponse)
def fetch_medical_profile(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = (
        db.query(MedicProfile).filter(MedicProfile.owner_id == current_user.id).first()
    )
    if fetched is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Profile does not exist.",
        )

    return fetched


@router.post("/medicals", status_code=status.HTTP_200_OK, response_model=MedicResponse)
def create_medical_profile(
    medic_profile: MedicIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_profile = MedicProfile(
        **medic_profile.model_dump(exclude_unset=True), owner_id=current_user.id
    )

    db.add(new_profile)

    try:
        db.commit()
        db.refresh(new_profile)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can only have one profile.",
        )

    return new_profile


@router.patch("/medicals", status_code=status.HTTP_200_OK, response_model=MedicResponse)
def update_medical_profile(
    updated: MedicIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    to_update = (
        db.query(MedicProfile).filter(MedicProfile.owner_id == current_user.id).first()
    )

    if not to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Profile does not exist.",
        )

    dict_update = updated.model_dump(exclude_unset=True)

    if not dict_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in dict_update.items():
        setattr(to_update, key, value)

    to_update.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(to_update)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An error occured."
        )

    return to_update


@router.delete("/medicals", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_profile(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    to_delete = (
        db.query(MedicProfile).filter(MedicProfile.owner_id == current_user.id).first()
    )

    if to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Profile does not exist.",
        )

    db.delete(to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
