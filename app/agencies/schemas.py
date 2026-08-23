from pydantic import BaseModel, ConfigDict, EmailStr

from app.agencies.models import OrgTypeEnum


class AgencyOut(BaseModel):
    name: str
    email: EmailStr
    phone: str
    org_type: OrgTypeEnum
    org_address: str
    latitude: float
    longitude: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
