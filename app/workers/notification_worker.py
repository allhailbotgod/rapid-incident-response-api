from datetime import datetime, timezone
import json

from sqlalchemy.orm import Session

from app.database import local_session
from app.notifications.models import (
    NotificationChannel,
    NotificationStatus,
    Notifications,
)
from app.services.firebase_service import send_push_notification
from app.services.notification_service import get_push_tokens
from app.utils.redis import redis_client, NOTIFICATION_QUEUE
import app.models

MAX_RETRIES = 5


def send_push(notification: Notifications, db: Session):
    if not notification.recipient_email:
        raise ValueError("Push notification has no recipient email.")

    tokens = get_push_tokens(db=db, email=notification.recipient_email)

    if not tokens:
        raise ValueError(f"Tokens not found for {notification.recipient_email}.")

    for token in tokens:
        send_push_notification(
            device_token=token, title=notification.title, message=notification.message
        )


def send_sms(notification):
    print(f"SMS sending not implemented yet for " f"{notification.recipient_phone}")


def send_whatsapp(notification):
    print(
        f"WhatsApp sending not implemented yet for " f"{notification.recipient_phone}"
    )


def process_notification(db: Session, notification_id: str):
    notification = (
        db.query(Notifications).filter(Notifications.id == notification_id).first()
    )

    if notification is None:
        print(f"Notification: {notification_id} -> Not found!")
        return

    print(f"Processing {notification.channel.value} notification {notification.id}")

    try:
        if notification.channel == NotificationChannel.PUSH:
            send_push(notification=notification, db=db)

        elif notification.channel == NotificationChannel.SMS:
            send_sms(notification)

        elif notification.channel == NotificationChannel.WHATSAPP:
            send_whatsapp(notification)

        notification.status = NotificationStatus.SENT
        notification.sent_at = datetime.now(timezone.utc)
        notification.error = "No error occured"
        db.commit()

        print(f"Notification {notification.id} sent successfully.")

    except Exception as exc:

        db.rollback()

        notification.retry_count += 1
        notification.error = str(exc)

        if notification.retry_count < MAX_RETRIES:
            notification.status = NotificationStatus.PENDING

            db.commit()

            redis_client.rpush(
                NOTIFICATION_QUEUE,
                json.dumps({"notification_queue": str(notification.id)}),
            )

            print(
                f"Notification {notification.id} failed. "
                f"Retry {notification.retry_count}/{MAX_RETRIES} queued."
            )

        else:
            notification.status = NotificationStatus.FAILED

            db.commit()

            print(
                f"Notification {notification.id} permanently failed "
                f"after {MAX_RETRIES} attempts: {exc}"
            )


def start_worker():
    print("Notification worker started!")

    while True:
        job = redis_client.blpop(NOTIFICATION_QUEUE)

        if not job:
            continue

        _, payload = job

        data = json.loads(payload)

        notification_id = data["notification_queue"]

        db: Session = local_session()

        try:
            process_notification(
                db=db,
                notification_id=notification_id,
            )

        except Exception as exc:
            db.rollback()
            print(f"Error processing notification " f"{notification_id}: {exc}")

        finally:
            db.close()


if __name__ == "__main__":
    start_worker()
