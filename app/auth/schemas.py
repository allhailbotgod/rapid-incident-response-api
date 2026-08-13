from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from app.users.models import Gender


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class UserIn(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    phone: str
    email: EmailStr
    password: str
    gender: Gender


class RoleResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    gender: Gender
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)
