from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID


class RoleResponse(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserProfile(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str
    email: EmailStr
    role: RoleResponse
    phone: str
    gender: str

    model_config = ConfigDict(from_attributes=True)
