from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ContactIn(BaseModel):
    phone: str
    first_name: str
    middle_name: str | None
    last_name: str
    relationship: str


class ContactOut(ContactIn):
    pass


class SOSResponse(BaseModel):
    id: UUID
    first_name: str
    middle_name: str | None
    last_name: str
    phone: str
    relationship: str

    model_config = ConfigDict(from_attributes=True)
