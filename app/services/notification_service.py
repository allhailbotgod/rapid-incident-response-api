from sqlalchemy.orm import Session

from app.notifications.models import (
    Notifications,
    NotificationChannel,
    NotificationStatus,
)
from app.sos.models import SOS
from app.users.models import Users


def create_notification(
    db: Session,
    incident_id,
    channel: NotificationChannel,
    title: str,
    message: str,
    recipient_email: str | None = None,
    recipient_phone: str | None = None,
) -> Notifications:

    notification = Notifications(
        incident_id=incident_id,
        channel=channel,
        status=NotificationStatus.PENDING,
        recipient_email=recipient_email,
        recipient_phone=recipient_phone,
        title=title,
        message=message,
    )

    db.add(notification)

    return notification


def notify_sos_contacts(
    db: Session,
    incident_id,
    owner_id,
    title: str,
    message: str,
):
    sos_contacts = db.query(SOS).filter(SOS.owner_id == owner_id).all()

    for sos in sos_contacts:

        # SMS
        create_notification(
            db=db,
            incident_id=incident_id,
            channel=NotificationChannel.SMS,
            title=title,
            message=message,
            recipient_phone=sos.phone,
        )

        # WhatsApp
        create_notification(
            db=db,
            incident_id=incident_id,
            channel=NotificationChannel.WHATSAPP,
            title=title,
            message=message,
            recipient_phone=sos.phone,
        )

        # Check whether the SOS contact has an RIR account
        if sos.email:
            user = db.query(Users).filter(Users.email == sos.email).first()

            if user:
                create_notification(
                    db=db,
                    incident_id=incident_id,
                    channel=NotificationChannel.PUSH,
                    title=title,
                    message=message,
                    recipient_email=user.email,
                )
