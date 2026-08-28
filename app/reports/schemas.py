from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.reports.models import ReportPriority, ReportStatus, ReportType


class MediaUpload(BaseModel):
    filename: str
    content_type: str


class MediaOut(BaseModel):
    id: UUID = Field(alias="media_id")
    object_key: str
    content_type: str
    upload_status: str

    model_config = ConfigDict(
        from_attributes=True, validate_by_alias=True, validate_by_name=True
    )


class IncidentCreate(BaseModel):
    latitude: float
    longitude: float
    report_type: ReportType
    description: str | None = None
    media: list[MediaUpload]


class IncidentResponse(BaseModel):
    id: UUID = Field(alias="incident_id")
    reporter_id: UUID
    latitude: float
    longitude: float
    report_type: ReportType
    priority: ReportPriority
    status: ReportStatus
    description: str
    media: list[MediaOut]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True, validate_by_alias=True, validate_by_name=True
    )
