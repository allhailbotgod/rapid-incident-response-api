from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.users.models import Users
from app.users.schemas import ProfileUpdate, UserProfile

router = APIRouter()


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserProfile)
def fetch_profile(
    db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)
):
    fetched = db.query(Users).filter(Users.id == current_user.id).first()
    return fetched


@router.patch("/profile", status_code=status.HTTP_200_OK, response_model=UserProfile)
def update_profile(
    updated: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    to_update = db.query(Users).filter(Users.email == current_user.email).first()

    if not to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
        )

    check_empty_input = updated.model_dump(exclude_unset=True)

    if not check_empty_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in check_empty_input.items():
        setattr(to_update, key, value)

    try:
        db.commit()
        db.refresh(to_update)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An error occured."
        )

    return to_update


@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    confirmation: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    if confirmation != "DELETE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmation error."
        )

    try:
        db.delete(current_user)
        db.commit()

    finally:
        pass

    return Response(status_code=status.HTTP_204_NO_CONTENT)
