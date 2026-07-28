from pydantic import BaseModel


class RolesOut(BaseModel):
    name: str
    created_at: str


class RolesIn(BaseModel):
    name: str
