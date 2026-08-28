from uuid import uuid4
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

from app.config import settings

month = datetime.now().month.strftime("%m")
year = datetime.now().year.strftime("%Y")

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
    config=Config(signature_version="s3v4"),
)


def create_upload_url(filename: str, content_type: str):
    extension = filename.rsplit(".", 1)[-1]
    object_key = f"incidents/{year}/{month}/{uuid4()}.{extension}"

    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=600,
    )

    return {"upload_url": upload_url, "object_key": object_key}


def create_download_url(object_key: str):

    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": object_key,
        },
        ExpiresIn=300,
    )


def verify_object_exists(object_key: str) -> bool:
    try:
        s3_client.head_object(
            Bucket=settings.S3_BUCKET,
            Key=object_key,
        )
        return True
    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")

        if error_code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise
