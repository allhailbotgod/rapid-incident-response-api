from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.agencies.models import Agency
from app.agencies.schemas import (
    AgencyOut,
    AgencyIn,
    AgencyUpdate,
)
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.reports.models import Incidents
from app.roles.models import Roles
from app.users.models import Users
from app.utils.helpers import require_admin

router = APIRouter(prefix="/agencies")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AgencyOut])
def fetch_organizations(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    fetched = db.query(Agency).all()

    return fetched


@router.get(
    "/incidents", status_code=status.HTTP_200_OK, response_model=list[AgencyOut]
)
def fetch_agency_specific_incidents(
    db: Session = Depends(get_db), current_user: Users = Depends(require_admin)
):
    incidents = (
        db.query(Incidents).filter(Incidents.agency_id == current_user.org_id).all()
    )

    return incidents


@router.post("/register", status_code=status.HTTP_200_OK, response_model=AgencyOut)
def register_organization(
    data: AgencyIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_agency = Agency(**data.agency.model_dump())

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


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=AgencyOut)
def update_organization_details(
    id: UUID,
    updates: AgencyUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_admin),
):
    to_update = (
        db.query(Agency)
        .filter(Agency.id == id, current_user.org_id == Agency.id)
        .first()
    )

    if not to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization does not exist."
        )

    check_empty_input = updates.model_dump(exclude_unset=True)

    if not check_empty_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    for key, value in check_empty_input.items():
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_admin),
):
    to_delete = (
        db.query(Agency)
        .filter(Agency.id == id, Agency.id == current_user.org_id)
        .first()
    )

    if not to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization does not exist."
        )

    try:
        db.delete(to_delete)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An error occured."
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
