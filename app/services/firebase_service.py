import firebase_admin
from firebase_admin import credentials, messaging

from app.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)


def send_push_notification(device_token: str, title: str, message: str):
    notification = messaging.Notification(title=title, body=message)

    message_data = messaging.Message(notification=notification, fid=device_token)

    return messaging.send(message_data)
