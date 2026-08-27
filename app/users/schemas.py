from pydantic import BaseModel, ConfigDict, EmailStr


class RoleResponse(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    role: RoleResponse
    phone: str
    gender: str

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    gender: str | None = None
