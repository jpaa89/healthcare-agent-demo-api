from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.domain.ehr_ingestion.ehr_context_models import EHRContextItem


class EHRQuery(BaseModel):
    query: str


class EHRQueryOutput(BaseModel):
    answer: str
    references: list[EHRContextItem]


class EHRContextIds(BaseModel):
    ids: list[UUID]
    model_config = ConfigDict(extra="forbid")
