from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class RolesOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RolesIn(BaseModel):
    name: str | None = None
