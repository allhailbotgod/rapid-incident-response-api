from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.reports.models import Media, ReportType, Reports
from app.reports.schemas import IncidentCreate, IncidentResponse
from app.services.notification_service import notify_sos_contacts
from app.sos.models import SOS
from app.storage import create_upload_url, verify_object_exists
from app.users.models import Users
from app.config import settings
from app.utils.helpers import require_dispatch

router = APIRouter()


ALLOWED_MEDIA_TYPES = settings.ALLOWED_MEDIA_TYPES


@router.get(
    "/incidents", status_code=status.HTTP_200_OK, response_model=list[IncidentResponse]
)
def fetch_incidents(
    db: Session = Depends(get_db), current_user=Depends(require_dispatch)
):
    fetched = db.query(Reports).all()

    return fetched


@router.post("/incidents", status_code=status.HTTP_201_CREATED)
def report_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    new_incident = Reports(
        **data.model_dump(exclude={"media"}), reporter_id=current_user.id
    )

    try:
        db.add(new_incident)
        db.flush()

        if data.report_type == ReportType.VICTIM:
            notify_sos_contacts(
                db=db,
                incident_id=new_incident.id,
                owner_id=current_user.id,
                title="Emergency Alert!",
                message=f"{current_user.first_name} {current_user.last_name} has reported an emergency ({data.report_summary.value}) and is requesting immediate assistance. Last known Location: {data.latitude} {data.longitude}.",
            )

        upload_urls = []

        for media in data.media:
            if media.content_type not in ALLOWED_MEDIA_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported media type: {media.content_type}",
                )

            upload_url, object_key = create_upload_url(
                filename=media.filename, content_type=media.content_type
            )

            new_media = Media(
                incident_id=new_incident.id,
                object_key=object_key,
                content_type=media.content_type,
            )

            db.add(new_media)
            db.flush()

            upload_urls.append(
                {
                    "media_id": new_media.id,
                    "object_key": object_key,
                    "upload_url": upload_url,
                    "content_type": media.content_type,
                }
            )

        db.commit()
        db.refresh(new_incident)

        return {
            "incident_id": new_incident.id,
            "status": new_incident.status,
            "upload_urls": upload_urls,
        }

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create incident.",
        )

    except Exception as e:
        db.rollback()
        print("error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the incident.",
        )


@router.post(
    "/incidents/{incident_id}/media/{media_id}/confirm", status_code=status.HTTP_200_OK
)
def confirm_media_upload(
    incident_id: UUID,
    media_id: UUID,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    to_update = (
        db.query(Media)
        .join(Reports)
        .filter(
            Media.id == media_id,
            Media.incident_id == incident_id,
            Reports.reporter_id == current_user.id,
        )
        .first()
    )

    if to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Media not found."
        )

    try:
        exists = verify_object_exists(to_update.object_key)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not verify media upload.",
        )

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media has not been uploaded.",
        )

    try:
        to_update.upload_status = "uploaded"

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Could not update status."
        )

    return {"message": "Upload successful."}
