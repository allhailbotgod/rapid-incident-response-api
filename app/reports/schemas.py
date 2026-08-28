from pydantic import BaseModel

from app.reports.models import ReportType


class MediaUpload(BaseModel):
    filename: str
    content_type: str


class IncidentCreate(BaseModel):
    latitude: float
    longitude: float
    report_type: ReportType
    description: str | None = None
    media: list[MediaUpload] = []
