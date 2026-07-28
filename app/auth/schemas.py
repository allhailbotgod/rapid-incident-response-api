from pydantic import BaseModel, EmailStr


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class UserIn(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    phone: int
    email: EmailStr
    gender: str
    role_id: int
