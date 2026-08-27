from pydantic import BaseModel, ConfigDict, EmailStr
from app.agencies.models import OrgTypeEnum
from uuid import UUID


class AgencyBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    org_type: OrgTypeEnum
    org_address: str
    latitude: float
    longitude: float
    is_active: bool


class AgencyOut(AgencyBase):
    id: UUID
    pass

    model_config = ConfigDict(from_attributes=True)


class AgencyIn(AgencyBase):
    pass


class AgencyUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    org_type: OrgTypeEnum | None = None
    org_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None


class AgencyRegistration(BaseModel):
    agency: AgencyIn
    email: EmailStr