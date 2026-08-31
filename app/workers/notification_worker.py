from datetime import datetime, timezone
import json

from sqlalchemy.orm import Session

from app.database import local_session
from app.notifications.models import NotificationStatus, Notifications
from app.utils.redis import redis_client, NOTIFICATION_QUEUE
from app.reports.models import Reports


def process_notification(db: Session, notification_id: str):
    notification = (
        db.query(Notifications).filter(Notifications.id == notification_id).first()
    )

    if notification is None:
        print(f"Notification: {notification_id} -> Not found!")
        return

    print(f"Processing {notification.channel.value} notification {notification.id}")

    notification.status = NotificationStatus.SENT
    notification.sent_at = datetime.now(timezone.utc)

    db.commit()

    print(f"Notification {notification.id} sent successfully.")


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
