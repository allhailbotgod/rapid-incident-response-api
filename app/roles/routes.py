from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.roles.models import Roles
from app.roles.schemas import RolesIn, RolesOut
from app.users.models import Users

router = APIRouter()


@router.post("/roles", status_code=status.HTTP_200_OK, response_model=RolesOut)
async def create_roles(
    role: RolesIn, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    user = (
        db.query(Users)
        .join(Roles, Users.role_id == Roles.id)
        .filter(Users.id == current_user.id, Roles.name == "admin")
        .first()
    )

    if not user:
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
