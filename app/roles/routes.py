from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from uuid import UUID
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.roles.models import Roles
from app.roles.schemas import RolesIn, RolesOut
from app.users.models import Users

router = APIRouter()


@router.get("/roles", status_code=status.HTTP_200_OK, response_model=list[RolesOut])
def fetch_roles(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized."
        )

    roles = db.query(Roles).all()

    return roles


@router.post("/roles", status_code=status.HTTP_200_OK, response_model=RolesOut)
def create_roles(
    role: RolesIn, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized."
        )

    new_role = Roles(**role.model_dump())

    db.add(new_role)

    try:
        db.commit()
        db.refresh(new_role)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role already exists."
        )

    return new_role


@router.patch("/roles/{id}", status_code=status.HTTP_200_OK, response_model=RolesOut)
def update_role(
    id: UUID,
    role_update: RolesIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required."
        )

    to_update = db.query(Roles).filter(Roles.id == id).first()

    if to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found."
        )

    dict_update = role_update.model_dump(exclude_unset=True)

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
