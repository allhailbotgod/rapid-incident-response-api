from pydantic import BaseModel, ConfigDict
from app.medic.models import BloodgroupEnum, GenotypeEnum


class MedicIn(BaseModel):
    blood_group: BloodgroupEnum | None = None
    genotype: GenotypeEnum | None = None
    conditions: list[str] | None = None
    allergies: list[str] | None = None


class MedicResponse(BaseModel):
    blood_group: BloodgroupEnum | None = None
    genotype: GenotypeEnum | None = None
    conditions: list[str] | None = None
    allergies: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)
