from enum import Enum
from pydantic import BaseModel, EmailStr


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


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
    gender: GenderEnum


class RoleResponse(BaseModel):
    name: str


class UserOut(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    gender: str
    role: RoleResponse
