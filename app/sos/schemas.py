from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from app.sos.models import SOS_Relation


class ContactIn(BaseModel):
    phone: str
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr | None = None
    relationship: SOS_Relation


class ContactOut(ContactIn):
    pass

    model_config = ConfigDict(from_attributes=True)


class SOSResponse(BaseModel):
    id: UUID
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr | None = None
    phone: str
    relationship: str

    model_config = ConfigDict(from_attributes=True)


class SOSPatch(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    relationship: SOS_Relation | None = None
