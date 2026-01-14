from datetime import date, datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel
from enum import StrEnum, auto


class EHRContextType(StrEnum):
    DEMOGRAPHICS = auto()
    CHRONIC_CONDITION = auto()
    ALLERGY = auto()
    MEDICATION = auto()
    VISIT = auto()
    LAB_RESULT = auto()


class EHRSourceType(StrEnum):
    DEMOGRAPHICS = auto()
    MEDICAL_HISTORY = auto()
    DOCTOR = auto()
    LAB_TEST = auto()


class EHRContextSource(BaseModel):
    type: EHRSourceType
    recorded_at: Optional[date]
    recorded_by: Optional[str]


class EHRContextItem(BaseModel):
    id: UUID
    patient_id: str
    type: EHRContextType
    content: str
    data: Optional[Dict[str, Any]] = None
    source: EHRContextSource
    created_at: datetime  # for audit, not to be used as part of context
