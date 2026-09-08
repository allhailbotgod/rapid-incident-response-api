from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.devices.models import UserDevices
from app.devices.schemas import DeviceTokenIn
from app.users.models import Users

router = APIRouter(prefix="/devices")


@router.post("/register", status_code=status.HTTP_200_OK)
def register_device_token(
    data: DeviceTokenIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    existing_device = db.query(UserDevices).filter(
        UserDevices.device_token == data.device_token
    )

    if existing_device:
        existing_device.owner_id = current_user.id
        existing_device.platform = data.platform

    else:
        new_device = UserDevices(
            owner_id=current_user.id,
            device_token=data.device_token,
            platform=data.platform,
        )

        db.add(new_device)

    db.commit()

    return {"message": "Device registered successfully."}
